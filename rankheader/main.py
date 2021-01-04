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
from core.gather import Gatherer
from core.analyze import Analyzer
from core.timer import Timer

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

async def main_async(data_path, num_top, num_sites, http_timeout):
    '''
    Main routine is main entry point of program.
    '''
    with Timer() as program_timer:
        with Timer() as gather_timer:
            site_info = await Gatherer.get_site_info_async(data_path, num_sites, http_timeout)
        logging.info(f'--- gather duration: {gather_timer.interval}')
        
        with Timer() as analysis_timer:
            site_report = Analyzer.get_site_report(site_info)
        logging.info(f'--- site analysis duration: {analysis_timer.interval} seconds ---')
        logging.info(f'--- site analysis report: --- \n{site_report}')

        with Timer() as analysis_timer:
            header_report = Analyzer.get_header_report(site_info, num_top)
        logging.info(f'--- header analysis duration: {analysis_timer.interval} seconds ---')
        logging.info(f'--- header analysis report: --- \n{header_report}')

    logging.info(f'--- program duration: {program_timer.interval} seconds ---')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate top 10 header stats', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_path', default='../data/top-1m.csv', help='Path to data file (top-1m.csv)')
    parser.add_argument('--num_headers', default=10, type=int, help='Number of headers to take as top rank')
    parser.add_argument('--num_sites', default=1000, type=int, help='Number of sites to analyze')
    parser.add_argument('--http_timeout', default=10, type=int, help='Request timeout (sec)')
    arg = parser.parse_args()

    asyncio.run(main_async(
        arg.data_path,
        arg.num_headers,
        arg.num_sites,
        arg.http_timeout))