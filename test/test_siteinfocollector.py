import pytest
from src.siteinfocollector import SiteInfoCollector

class TestSiteInfoCollector(): 
    @pytest.fixture
    def num_top(self):
        return 2
    
    @pytest.fixture
    def expected_sites(self):
        sites = ['http://www.google.com', 'http://www.youtube.com']
        return sites

    @pytest.fixture
    def expected_sites_info(self):
        sites_info = [{
            'site': 'http://www.google.com',
            'status': 200,
            'headers': ['Date', 'Expires', 'Cache-Control', 'Content-Type', 'P3P', 'Content-Encoding', 'Server', 'Content-Length', 'X-XSS-Protection', 'X-Frame-Options', 'Set-Cookie', 'Set-Cookie']
        }, {
            'site': 'http://www.youtube.com',
            'status': 200,
            'headers': ['Content-Type', 'X-Content-Type-Options', 'Cache-Control', 'Pragma', 'Expires', 'Date', 'X-Frame-Options', 'Strict-Transport-Security', 'P3P', 'Content-Encoding', 'Server', 'X-XSS-Protection', 'Set-Cookie', 'Set-Cookie', 'Alt-Svc', 'Transfer-Encoding']
        }]
        return sites_info

    def test_get_top_sites(self, num_top, expected_sites):
        actual_sites = list(SiteInfoCollector.get_top_sites('./data/top-1m.csv', num_top))
        assert actual_sites == expected_sites

    @pytest.mark.asyncio
    async def test_get_site_info_async(self, num_top, expected_sites_info):
        actual_sites_info = list(await SiteInfoCollector.get_site_info_async('./data/top-1m.csv', num_top, 2, 30))
        assert actual_sites_info == expected_sites_info
        