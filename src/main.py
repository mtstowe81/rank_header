# Program that analyzes HTTP responses from the top 1000 sites from a list of sites. 
#
# Outputs:
# - The top 10 HTTP response headers and the percentage of sites in which each of those 10 headers appeared 
# - Total Duration of the Program 

import sys
import time
import logging
import argparse
import asyncio
from core.siteinfocollector import SiteInfoCollector
from core.siteinfoanalyzer import SiteInfoAnalyzer
from core.siteinfotimer import SiteInfoTimer
from core.siteinfodisplay import SiteInfoDisplay

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logging.getLogger('backoff').setLevel(logging.FATAL)

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v == ('True'):
        return True
    elif v == ('False'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

async def main_async(data_path, num_top, num_sites, display_graph, http_concurrency, http_timeout):
    '''
    Main routine is main entry point of program.
    '''
    with SiteInfoTimer() as program_timer:
        with SiteInfoTimer() as gather_timer:
            site_info = await SiteInfoCollector.get_site_info_async(data_path, num_sites, http_concurrency, http_timeout)
        logging.info("--- collect duration: {0}".format(gather_timer.interval))
        
        with SiteInfoTimer() as analysis_timer:
            stats = SiteInfoAnalyzer.get_site_stats(site_info, num_top)
        logging.info("--- analysis duration: {0} seconds ---".format(analysis_timer.interval))
        
        if display_graph:
            SiteInfoDisplay.display_stats(stats)

    logging.info("--- program duration: {0} seconds ---".format(program_timer.interval))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate top 10 header stats', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--data_path', default='../data/top-1m.csv', help='Path to data file (top-1m.csv)')
    parser.add_argument('--num_headers', default=10, type=int, help='Number of headers to take as top rank')
    parser.add_argument('--num_sites', default=1000, type=int, help='Number of sites to analyze')
    parser.add_argument('--display_graph', default='True', type=str2bool, const=True, nargs='?', help='Display the graph', choices=[True, False])
    parser.add_argument('--http_concurrency', default=20, type=int, help='Number of concurrent requests')
    parser.add_argument('--http_timeout', default=30, type=int, help='Request timeout (sec)')

    arg = parser.parse_args()

    asyncio.run(main_async(
        arg.data_path,
        arg.num_headers,
        arg.num_sites,
        arg.display_graph,
        arg.http_concurrency,
        arg.http_timeout))