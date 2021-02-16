import pandas as pd

class Analyzer:
    '''
    Get the top N sites stats from the provided data file.
    '''

    @staticmethod
    def get_site_report(sites):
        '''
        Get site stats from sites.

        Analyzes HTTP responses from the sites provided. 
        - Gets the count of each response type that was observed.

        Parameters
        ----------
        sites: str[]
            List of sites to analyze results for.

        Returns
        -------
        string
            A string representing the analysis results for sites.
            The format of the string provides the following stats:
            - rank: integer representing rank (leftmost unlabeled column)
            - result: type of the result (success, error, etc)
            - total: the total of the result type
        '''
        sites_df = pd.DataFrame(sites)
        sites_errors_df = (sites_df
            .groupby(by=['result'])
            .size()
            .reset_index(name='total')
            .sort_values(['total'],ascending=[False])
            .reset_index(drop=True))
        sites_errors_df.index += 1
        return sites_errors_df.to_string()

    @staticmethod
    def get_header_report(sites, num_top):
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
        string
            A string representing the analysis results for headers.
            The format of the string provides the following stats:
            - rank: integer representing rank (leftmost unlabeled column)
            - header: header name
            - total_site_occurrences: total unique occurrences per site of a header for all sites
            - total_occurrences: total occurrences of a header for all sites, including multiple occurrences per site
            - percent_sites: percent of site occurrences based on total_site_occurrences
        '''
        top_sites_df = pd.DataFrame(sites)
        top_sites_df = top_sites_df[top_sites_df.result == 'Success']
        top_sites_df = top_sites_df.explode('headers')

        top_headers_unique_df = (top_sites_df
            .drop_duplicates(subset=['site', 'headers'])
            .groupby(by=['headers'])
            .size()
            .reset_index(name='total_site_occurrences'))

        top_headers_df = (top_sites_df
            .groupby(by=['headers'])
            .size()
            .reset_index(name='total_occurrences'))

        stats_df = (pd
            .merge(top_headers_unique_df, top_headers_df, on='headers')
            .sort_values(['total_site_occurrences', 'total_occurrences'],ascending=[False, False])
            .head(num_top)
            .reset_index(drop=True))
        stats_df.rename(columns={'headers':'header'}, inplace=True)
        stats_df.index += 1
        
        num_sites = len(sites)
        stats_df['percent_sites'] = stats_df.apply(lambda row: ((row.total_site_occurrences/num_sites)*100), axis=1)
        return stats_df.to_string()