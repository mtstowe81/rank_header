import sys
import backoff
import aiohttp
import asyncio
import logging
import time

class SiteInfoCollector:
    '''
    Get the headers for top N sites from the provided data file.
    '''

    @staticmethod
    async def get_site_info_async(data_path, num_sites, http_concurrency, http_timeout):
        '''
        Get all the site information for analysis.

        Parameters
        ----------
        data_path: str
            Path to file with a website per line.
        num_sites: int
            The top number of sites to read from the data_path.
        http_concurrency: int
            The number of concurrent HTTP requests to allow.
        http_timeout: int
            The timeout for each HTTP request submitted.

        Returns
        -------
        dictionary
            A dictionary with the following key/value structure
            { 'site': str, 'status' : [int|None], 'headers' : [str[]|None] }
        '''
        sites = SiteInfoCollector.__get_top_sites(data_path, num_sites)
        return await SiteInfoCollector.__get_all_site_response_headers_async(sites, http_concurrency, http_timeout)

    @staticmethod
    def __get_top_sites(data_path, num_sites):
        '''
        Get top sites from the data path.
        '''
        with open(data_path, "r") as data_file:
            for idx,line in enumerate(data_file, 1):
                yield 'http://www.' + line.split(',')[1].strip()
                
                if idx == num_sites:
                    break

    @staticmethod
    @backoff.on_exception(backoff.expo, (asyncio.TimeoutError), max_time=120)
    async def __get_site_response_headers_async_with_backoff(session, site):
        '''
        Get single site response headers asynchronously with backoff retry pattern.
        '''
        start_time = time.time()
        async with session.get(site) as response:
            duration = time.time() - start_time
            logging.debug("received site {0} {1}: {2} seconds".format(site, response.status, duration))
            return { 'site': site, 'status' : response.status, 'headers' : list(response.headers.keys()) }

    @staticmethod
    async def __get_site_response_headers_async(session, site, sem):
        '''
        Get single site response headers asynchronously.
        '''
        async with sem:
            logging.debug("requesting {0}".format(site))
            try:
                return await SiteInfoCollector.__get_site_response_headers_async_with_backoff(session, site)
            except:
                logging.error("Unexpected error for {0}: {1}".format(site, sys.exc_info()[0]))
                return { 'site': site, 'status' : None, 'headers' : None }

    @staticmethod
    async def __get_all_site_response_headers_async(sites, concurrency, timeout):
        '''
        Get all site response headers asynchronously.
        '''
        # using a semaphore as there appears to be some issue in aiohttp with
        # multiple concurrent requests.  the semaphore is used to limit the number
        # of requests we attempt to make at once until I can figure out what
        # is going on here.
        logging.info("getting site headers...")
        sem = asyncio.Semaphore(concurrency)
        timeout = aiohttp.ClientTimeout(total=timeout)
        connector = aiohttp.TCPConnector(ssl=False, limit=concurrency)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            return await asyncio.gather(*(SiteInfoCollector.__get_site_response_headers_async(session, site, sem) for site in sites))