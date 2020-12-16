import pytest
from src.siteinfoanalyzer import SiteInfoAnalyzer

class TestSiteInfoAnalyzer(): 
    def test_get_site_stats(self):
        sites = [
            {
                'site' : 'www.abc.com',
                'headers': {
                    'foo' : 'bar',
                    'bing' : 'bam'
                },
                'status' : None
            },
            {
                'site' : 'www.def.com',
                'headers': {
                    'foo' : 'bar',
                    'extra1' : 'extra1'
                },
                'status' : None
            },
            {
                'site' : 'www.ghi.com',
                'headers': {
                    'foo' : 'bar',
                },
                'status' : None
            },
            {
                'site' : 'www.jkl.com',
                'headers': {
                    'bing' : 'bam'
                },
                'status' : None
            },
            {
                'site' : 'www.mno.com',
                'headers': {
                    'foo' : 'bar',
                    'bing' : 'bam',
                    'extra2' : 'extra2'
                },
                'status' : None
            }
        ]
        num_top = 2

        results = SiteInfoAnalyzer.get_site_stats(sites, num_top)

        assert 'foo' in results
        assert 'bing' in results
        assert len(results) == 2

        foo = results['foo']
        assert foo['rank'] == 1
        assert foo['total_occurrences'] == 4
        assert foo['total_site_occurrences'] == 4
        assert foo['percent_site_occurrences'] == 80

        bing = results['bing']
        assert bing['rank'] == 2
        assert bing['total_occurrences'] == 3
        assert bing['total_site_occurrences'] == 3
        assert bing['percent_site_occurrences'] == 60
