import pytest
from rankheader.core.analyze import Analyzer

class TestAnalyzer():
    @pytest.fixture
    def num_top(self):
        return 2

    @pytest.fixture
    def sites(self):
        sites = [
            {
                'site' : 'www.abc.com',
                'headers': ['foo', 'bing'],
                'status' : 200,
                'result' : 'Success'
            },
            {
                'site' : 'www.def.com',
                'headers': ['foo', 'extra1'],
                'status' : 200,
                'result' : 'Success'
            },
            {
                'site' : 'www.ghi.com',
                'headers': ['foo'],
                'status' : 200,
                'result' : 'Success'
            },
            {
                'site' : 'www.jkl.com',
                'headers': ['bing'],
                'status' : 200,
                'result' : 'Success'
            },
            {
                'site' : 'www.mno.com',
                'headers': ['foo', 'bing', 'extra2'],
                'status' : 200,
                'result' : 'Success'
            }
        ]
        return sites

    @pytest.fixture
    def expected_header_stats(self):
        return '  header  total_site_occurrences  total_occurrences  percent_sites\n1    foo                       4                  4           80.0\n2   bing                       3                  3           60.0'

    @pytest.fixture
    def expected_site_stats(self):
        return '    result  total\n1  Success      5'
    
    def test_get_site_stats(self, sites, expected_site_stats):
        actual_stats = Analyzer.get_site_report(sites)
        assert actual_stats == expected_site_stats

    def test_get_header_stats(self, sites, num_top, expected_header_stats):
        actual_stats = Analyzer.get_header_report(sites, num_top)
        assert actual_stats == expected_header_stats