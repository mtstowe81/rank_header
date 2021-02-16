import sys
import backoff
import aiohttp
import asyncio
import logging

class Gatherer:
    '''
    Get the headers for top N sites from the provided data file.
    '''

    @staticmethod
    async def get_site_info_async(data_path, num_sites, http_timeout):
        '''
        Get all the site information for analysis.

        Parameters
        ----------
        data_path: str
            Path to file with a website per line.
        num_sites: int
            The top number of sites to read from the data_path.
        http_timeout: int
            The timeout for each HTTP request submitted.

        Returns
        -------
        dictionary
            A dictionary with the following key/value structure
            { 'site': str, 'status' : [int|None], 'headers' : [str[]|None] }
        '''
        sites = Gatherer.__get_top_sites(data_path, num_sites)
        return await Gatherer.__get_all_site_response_headers_async(sites, http_timeout)

    @staticmethod
    def __get_top_sites(data_path, num_sites):
        '''
        Get top sites from the data path.
        '''
        with open(data_path, "r") as data_file:
            for idx,line in enumerate(data_file, 1):
                yield 'https://www.' + line.split(',')[1].strip()
                
                if idx == num_sites:
                    break

    @staticmethod
    async def __get_site_response_headers_async(session, site):
        '''
        Get single site response headers asynchronously.
        '''
        logging.debug("requesting {0}".format(site))
        try:
            async with session.head(site) as response:
                return { 
                    'site': site, 'status' : response.status, 'headers' : list(response.headers.keys()), 'result' : 'Success' }
        except Exception as e:
            logging.debug("Unexpected error for {0}: {1}".format(site, e))
            return { 'site': site, 'status' : None, 'headers' : None, 'result' : type(e).__name__ }

    @staticmethod
    async def __get_all_site_response_headers_async(sites, timeout):
        '''
        Get all site response headers asynchronously.
        '''
        logging.info("getting site headers...")
        timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            return await asyncio.gather(*(Gatherer.__get_site_response_headers_async(session, site) for site in sites))