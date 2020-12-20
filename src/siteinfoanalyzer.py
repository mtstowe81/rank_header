import sys
import logging
import time
from matplotlib import pyplot as plt
import numpy as np
from itertools import zip_longest
import pandas as pd

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
        
        top_sites_df = pd.DataFrame(sites)
        top_sites_df = top_sites_df[top_sites_df.status != None]
        top_sites_df = top_sites_df.explode('headers')

        top_headers_unique_df = (top_sites_df
            .drop_duplicates(subset=['site', 'headers'])
            .groupby(by=["headers"])
            .size()
            .reset_index(name='total_site_occurrences'))

        top_headers_df = (top_sites_df
            .groupby(by=["headers"])
            .size()
            .reset_index(name='total_occurrences'))

        stats_df = (pd
            .merge(top_headers_unique_df, top_headers_df, on='headers')
            .sort_values(['total_site_occurrences', 'total_occurrences'],ascending=[False, False])
            .head(num_top)
            .reset_index(drop=True))
        
        num_sites = len(sites)
        stats_df['percent_sites'] = stats_df.apply(lambda row: ((row.total_site_occurrences/num_sites)*100), axis=1)
        stats_dict = (
            { value['headers']:
                {   
                    'rank': key+1,
                    'total_occurrences' : value['total_occurrences'],
                    'total_site_occurrences' : value['total_site_occurrences'],
                    'percent_site_occurrences' : value['percent_sites']
                }
                for (key,value) in stats_df.to_dict('index').items() })

        return stats_dict

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