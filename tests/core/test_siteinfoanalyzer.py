import pytest
from rankheader.core.siteinfoanalyzer import SiteInfoAnalyzer

class TestSiteInfoAnalyzer():
    @pytest.fixture
    def num_top(self):
        return 2

    @pytest.fixture
    def sites(self):
        sites = [
            {
                'site' : 'www.abc.com',
                'headers': ['foo', 'bing'],
                'status' : 200
            },
            {
                'site' : 'www.def.com',
                'headers': ['foo', 'extra1'],
                'status' : 200
            },
            {
                'site' : 'www.ghi.com',
                'headers': ['foo'],
                'status' : 200
            },
            {
                'site' : 'www.jkl.com',
                'headers': ['bing'],
                'status' : 200
            },
            {
                'site' : 'www.mno.com',
                'headers': ['foo', 'bing', 'extra2'],
                'status' : 200
            }
        ]
        return sites

    @pytest.fixture
    def expected_stats(self):
        stats = {
            'foo': {
                'rank': 1,
                'total_occurrences': 4,
                'total_site_occurrences': 4,
                'percent_site_occurrences': 80.0
            },
            'bing': {
                'rank': 2,
                'total_occurrences': 3,
                'total_site_occurrences': 3,
                'percent_site_occurrences': 60.0
            }
        }
        return stats
    
    def test_get_site_stats(self, sites, num_top, expected_stats):
        actual_stats = SiteInfoAnalyzer.get_site_stats(sites, num_top)
        assert actual_stats == expected_stats