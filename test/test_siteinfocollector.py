import pytest
from src.siteinfocollector import SiteInfoCollector

class TestSiteInfoCollector(): 
    def test_get_top_sites(self):
        sites = list(SiteInfoCollector.get_top_sites('./data/top-1m.csv', 2))
        
        assert len(sites) == 2
        assert sites[0] == 'http://www.google.com'
        assert sites[1] == 'http://www.youtube.com'

    @pytest.mark.asyncio
    async def test_get_site_info_async(self):
        sites = list(await SiteInfoCollector.get_site_info_async('./data/top-1m.csv', 2, 2, 30))
        
        assert len(sites) == 2
        assert sites[0]['site'] == 'http://www.google.com'
        assert sites[0]['headers'] != None
        assert sites[0]['status'] != None

        assert sites[1]['site'] == 'http://www.youtube.com'
        assert sites[1]['headers'] != None
        assert sites[1]['status'] != None
