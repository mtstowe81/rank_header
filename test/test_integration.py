import pytest
from src.siteinfocollector import SiteInfoCollector
from src.siteinfoanalyzer import SiteInfoAnalyzer

class TestIntegration(): 
    @pytest.mark.asyncio
    async def test_get_site_info_async(self):
        sites = await SiteInfoCollector.get_site_info_async('./data/top-1m.csv', 5, 2, 30)

        assert len(sites) == 5
        assert sites[0]['site'] == 'http://www.google.com'
        assert sites[0]['headers'] != None
        assert sites[0]['status'] != None

        assert sites[1]['site'] == 'http://www.youtube.com'
        assert sites[1]['headers'] != None
        assert sites[1]['status'] != None

        assert sites[2]['site'] == 'http://www.tmall.com'
        assert sites[2]['headers'] != None
        assert sites[2]['status'] != None

        assert sites[3]['site'] == 'http://www.baidu.com'
        assert sites[3]['headers'] != None
        assert sites[3]['status'] != None

        assert sites[4]['site'] == 'http://www.qq.com'
        assert sites[4]['headers'] != None
        assert sites[4]['status'] != None

        num_top = 2

        results = SiteInfoAnalyzer.get_site_stats(sites, num_top)

        assert len(results) == 2
        assert 'Date' in results
        assert 'Cache-Control' in results

        date = results['Date']
        assert date['rank'] == 1
        assert date['total_occurrences'] == 5
        assert date['total_site_occurrences'] == 5
        assert date['percent_site_occurrences'] == 100

        cache = results['Cache-Control']
        assert cache['rank'] == 2
        assert cache['total_occurrences'] == 5
        assert cache['total_site_occurrences'] == 5
        assert cache['percent_site_occurrences'] == 100

