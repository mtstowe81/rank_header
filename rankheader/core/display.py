from matplotlib import pyplot as plt
import numpy as np
from collections import deque

class Display:
    '''
    Displays the top N sites stats from the provided data file.
    '''

    @staticmethod
    def display_stats(stats):
        '''
        Display the stats from site and header analysis.

        Parameters
        ----------
        stats: dictionary
            A dictionary with the following key/value structure
            header_name : {
                'rank': int,
                'total_occurrences' : int,
                'total_site_occurrences' : int,
                'percent_site_occurrences' : int
            }
        '''
        topHeaders = deque()
        topHeaderPercents = deque()
        for stat in stats:
            topHeaders.appendleft(stat)
            topHeaderPercents.appendleft(stats[stat]['percent_site_occurrences'])
        
        plt.style.use('ggplot')
        plt.figure(figsize=(15,5))
        y_pos = np.arange(len(topHeaders))
        plt.barh(y_pos, topHeaderPercents, color='green')
        plt.ylabel("Header")
        plt.xlabel("Percent Sites")
        plt.title("Top Headers with Percent Site Occurrence")
        plt.yticks(y_pos, topHeaders)
        plt.show()