import pytest
from rankheader.core.gather import Gatherer

class TestGatherer(): 
    @pytest.fixture
    def num_top(self):
        return 1
    
    @pytest.fixture
    def expected_sites_info(self):
        sites_info = [{
            'site': 'https://www.google.com',
            'status': 200,
            'result' : 'Success',
            'headers': ['Date', 'Expires', 'Cache-Control', 'Content-Type', 'P3P', 'Content-Encoding', 'Server', 'Content-Length', 'X-XSS-Protection', 'X-Frame-Options', 'Set-Cookie', 'Set-Cookie']
        }]
        return sites_info

    @pytest.mark.asyncio
    async def test_get_site_info_async(self, num_top, expected_sites_info):
        actual_sites_info = list(await Gatherer.get_site_info_async('./data/top-1m.csv', num_top, 10))
        assert len(actual_sites_info) == 1
        assert actual_sites_info[0]['site'] == expected_sites_info[0]['site']
        assert actual_sites_info[0]['status'] == expected_sites_info[0]['status']
        assert actual_sites_info[0]['result'] == expected_sites_info[0]['result']
        assert len(actual_sites_info[0]['headers']) > 0