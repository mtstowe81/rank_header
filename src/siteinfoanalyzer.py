import sys
import logging
import time
from matplotlib import pyplot as plt
import numpy as np
from itertools import zip_longest

class SiteInfoAnalyzer:
    '''
    Get the top N sites stats from the provided data file.
    '''
    @staticmethod
    def get_site_stats(sites, num_top):
        '''
        Get headers stats from sites.

        Analyzes HTTP responses from the top 1000 sites in that list. 
        - Gets the top 10 response headers that appeared for all the sites.
        - Then for each of the top 10 response headers get the percentage of sites they occurred in
        '''
        logging.info("getting site headers stats...")
        global_header_rank = {  }
        for site_response in sites:
            if site_response != None:
                if 'headers' in site_response and site_response['headers'] != None:
                    # track the occurrences of a header within a site
                    # some headers show up multiple times, which can skew results
                    site_header_rank = { }
                    for header in site_response['headers']:
                        if header in site_header_rank:
                            site_header_rank[header] += 1
                        else:
                            site_header_rank[header] = 1

                    # track the occurrences of a header for all sites
                    # total occurrences = sum of all occurrences (including multiple occurrences of each site)
                    # total site occurrences = the count of sites a header has occurred in
                    for header in site_header_rank:
                        if header in global_header_rank:
                            global_header_rank[header]['total_site_occurrences'] += 1
                            global_header_rank[header]['total_occurrences'] += site_header_rank[header]
                        else:
                            global_header_rank[header] = { 'total_site_occurrences' : 1, 'total_occurrences' : site_header_rank[header] }

        # sort the headers DESC so that we have the highest occurrences first
        sorted_headers = sorted(global_header_rank.items(), key=lambda x: int(x[1]['total_site_occurrences']), reverse=True)

        logging.info("calculating top headers stats...")
        top_stats = { }
        for idx,header_info in enumerate(sorted_headers):
            rank = idx+1
            header_name = header_info[0]
            total_site_occurrences = header_info[1]['total_site_occurrences']
            total_occurrences = header_info[1]['total_occurrences']
            percent = (total_site_occurrences/len(sites)) * 100
            logging.info("rank: {0} | header={1} | total_occurrences={2} | total_site_occurrences={3} | percent_site_occurrences={4}".format(rank, header_name, total_occurrences, total_site_occurrences, percent))
            top_stats[header_name] = {
                'rank' : rank,
                'total_occurrences' : total_occurrences,
                'total_site_occurrences' : total_site_occurrences,
                'percent_site_occurrences' : percent
            }
            if idx == (num_top-1):
                break

        return top_stats

    @staticmethod
    def display_stats(stats):
        topHeaders = []
        topHeaderPercents = []
        for stat in stats:
            topHeaders.append(stat)
            topHeaderPercents.append(stats[stat]['percent_site_occurrences'])

        # reverse into DESC order
        topHeaders.reverse()
        topHeaderPercents.reverse()

        plt.style.use('ggplot')
        plt.figure(figsize=(15,5))
        y_pos = np.arange(len(topHeaders))
        plt.barh(y_pos, topHeaderPercents, color='green')
        plt.ylabel("Header")
        plt.xlabel("Percent Sites")
        plt.title("Top 10 Headers with Percent Site Occurrence")
        plt.yticks(y_pos, topHeaders)
        plt.show()