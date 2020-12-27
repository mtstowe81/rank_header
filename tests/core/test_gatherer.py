import pytest
from rankheader.core.gather import Gatherer

class TestGatherer(): 
    @pytest.fixture
    def num_top(self):
        return 2
    
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

    @pytest.mark.asyncio
    async def test_get_site_info_async(self, num_top, expected_sites_info):
        actual_sites_info = list(await Gatherer.get_site_info_async('./data/top-1m.csv', num_top, 2, 30))
        assert actual_sites_info == expected_sites_info
        