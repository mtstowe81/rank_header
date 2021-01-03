import pandas as pd

class Analyzer:
    '''
    Get the top N sites stats from the provided data file.
    '''

    @staticmethod
    def get_site_stats(sites, num_top):
        '''
        Get headers stats from sites.

        Analyzes HTTP responses from the sites provided. 
        - Gets the num_top response headers that appeared for all the sites.
        - Then for each of the num_top response headers get the percentage of sites they occurred in.

        Parameters
        ----------
        sites: str[]
            List of sites to analyze headers for.
        num_top: int
            Top number of headers to analyze.

        Returns
        -------
        dictionary
            A dictionary with the following key/value structure
            header_name : {
                'rank': int,
                'total_occurrences' : int,
                'total_site_occurrences' : int,
                'percent_site_occurrences' : int
            }
        '''
        
        top_sites_df = pd.DataFrame(sites)
        top_sites_df = top_sites_df[top_sites_df.error == False]
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

        index = df.index
        number_of_rows = len(index)

        summary = {
            'total_sites' : num_sites,
            'sample size':  
            'header_stats': stats_dict
        }

        return stats_dict