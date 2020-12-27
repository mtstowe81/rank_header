import pytest
from rankheader.core.gather import Gatherer
from rankheader.core.analyze import Analyzer

class TestGatherAnalyze(): 
    @pytest.fixture
    def num_top(self):
        return 7

    @pytest.fixture
    def num_sites(self):
        return 10

    @pytest.fixture
    def expected_stats(self):
        stats = {
            'Content-Encoding': {
                'rank': 1,
                'total_occurrences': 10,
                'total_site_occurrences': 10,
                'percent_site_occurrences': 100.0
            },
            'Content-Type': {
                'rank': 2,
                'total_occurrences': 10,
                'total_site_occurrences': 10,
                'percent_site_occurrences': 100.0
            },
            'Date': {
                'rank': 3,
                'total_occurrences': 10,
                'total_site_occurrences': 10,
                'percent_site_occurrences': 100.0
            },
            'Cache-Control': {
                'rank': 4,
                'total_occurrences': 9,
                'total_site_occurrences': 9,
                'percent_site_occurrences': 90.0
            },
            'Server': {
                'rank': 5,
                'total_occurrences': 9,
                'total_site_occurrences': 9,
                'percent_site_occurrences': 90.0
            },
            'Connection': {
                'rank': 6,
                'total_occurrences': 8,
                'total_site_occurrences': 8,
                'percent_site_occurrences': 80.0
            },
            'Transfer-Encoding': {
                'rank': 7,
                'total_occurrences': 8,
                'total_site_occurrences': 8,
                'percent_site_occurrences': 80.0
            }
        }
        return stats

    @pytest.fixture
    def expected_sites(self):
        sites = [{
            'site': 'http://www.google.com',
            'status': 200,
            'headers': ['Date', 'Expires', 'Cache-Control', 'Content-Type', 'P3P', 'Content-Encoding', 'Server', 'Content-Length', 'X-XSS-Protection', 'X-Frame-Options', 'Set-Cookie', 'Set-Cookie']
        }, {
            'site': 'http://www.youtube.com',
            'status': 200,
            'headers': ['Content-Type', 'X-Content-Type-Options', 'Cache-Control', 'Pragma', 'Expires', 'Date', 'X-Frame-Options', 'Strict-Transport-Security', 'P3P', 'Content-Encoding', 'Server', 'X-XSS-Protection', 'Set-Cookie', 'Set-Cookie', 'Alt-Svc', 'Transfer-Encoding']
        }, {
            'site': 'http://www.tmall.com',
            'status': 200,
            'headers': ['Server', 'Content-Type', 'Transfer-Encoding', 'Connection', 'Vary', 'Date', 'Vary', 'Vary', 'x-server-id', 'realpath', 'Cache-Control', 'Etag', 'x-readtime', 'x-via', 'EagleEye-TraceId', 'Strict-Transport-Security', 'Timing-Allow-Origin', 'Ali-Swift-Global-Savetime', 'Via', 'Age', 'X-Cache', 'X-Swift-SaveTime', 'X-Swift-CacheTime', 'EagleId', 'Strict-Transport-Security', 'Content-Encoding']
        }, {
            'site': 'http://www.baidu.com',
            'status': 200,
            'headers': ['Bdpagetype', 'Bdqid', 'Cache-Control', 'Connection', 'Content-Encoding', 'Content-Type', 'Date', 'Expires', 'P3p', 'P3p', 'Server', 'Set-Cookie', 'Set-Cookie', 'Set-Cookie', 'Set-Cookie', 'Set-Cookie', 'Set-Cookie', 'Set-Cookie', 'Traceid', 'X-Ua-Compatible', 'Transfer-Encoding']
        }, {
            'site': 'http://www.qq.com',
            'status': 200,
            'headers': ['Content-Type', 'Server', 'Content-Encoding', 'Content-Length', 'Cache-Control', 'Expires', 'Date', 'Connection', 'Vary', 'Strict-Transport-Security']
        }, {
            'site': 'http://www.sohu.com',
            'status': 200,
            'headers': ['Content-Type', 'Transfer-Encoding', 'Connection', 'Server', 'Date', 'Cache-Control', 'X-From-Sohu', 'Referrer-Policy', 'Content-Encoding', 'FSS-Cache', 'FSS-Proxy']
        }, {
            'site': 'http://www.taobao.com',
            'status': 200,
            'headers': ['Server', 'Content-Type', 'Transfer-Encoding', 'Connection', 'Vary', 'Date', 'Vary', 'x-server-id', 'Cache-Control', 'Etag', 'x-readtime', 'x-via', 'EagleEye-TraceId', 'Strict-Transport-Security', 'Timing-Allow-Origin', 'Via', 'Ali-Swift-Global-Savetime', 'Age', 'X-Cache', 'X-Swift-SaveTime', 'X-Swift-CacheTime', 'Set-Cookie', 'EagleId', 'Content-Encoding']
        }, {
            'site': 'http://www.facebook.com',
            'status': 200,
            'headers': ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options', 'Strict-Transport-Security', 'Set-Cookie', 'Set-Cookie', 'Content-Encoding', 'Expires', 'Cache-Control', 'Vary', 'Pragma', 'x-fb-rlafr', 'Content-Type', 'X-FB-Debug', 'Date', 'Alt-Svc', 'Transfer-Encoding', 'Connection']
        }, {
            'site': 'http://www.360.cn',
            'status': 200,
            'headers': ['Server', 'Date', 'Content-Type', 'Last-Modified', 'Transfer-Encoding', 'Connection', 'Etag', 'Content-Encoding']
        }, {
            'site': 'http://www.jd.com',
            'status': 200,
            'headers': ['Date', 'Content-Type', 'Transfer-Encoding', 'Connection', 'Vary', 'Content-Language', 'Expires', 'Cache-Control', 'Content-Encoding', 'Server']
        }]
        return sites

    # Usually fails after a period of time as the websites change.
    @pytest.mark.asyncio
    @pytest.mark.skipif(True, reason="Typically fails due to inconsistent site results.")
    async def test_get_site_info_async(self, expected_stats, expected_sites, num_top, num_sites):
        actual_sites = await Gatherer.get_site_info_async('./data/top-1m.csv', num_sites, 2, 30)
        assert actual_sites == expected_sites
        actual_stats = Analyzer.get_site_stats(actual_sites, num_top)
        assert actual_stats == expected_stats