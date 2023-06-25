"""
Based on:
  - https://github.com/scrapy/scrapy/blob/2.8.0/tests/test_downloadermiddleware_httpauth.py
  - https://github.com/scrapy/scrapy/blob/2.8.0/tests/test_downloadermiddleware_cookies.py
"""
import unittest

from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request, Response
from scrapy.spiders import Spider

from scrapy_strava.middlewares.ratelimit import SimpleStravaRateLimitMiddleware


class SimpleStravaRateLimitMiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.mw = SimpleStravaRateLimitMiddleware()
        self.spider = Spider('foo')

    def tearDown(self):
        del self.mw

    def _get_spider_status(self):
        return getattr(self.spider, 'rate_limit_status', None)

    def test_resp_limited(self):
        req = Request('http://example.com')
        res = Response('http://example.com', 
                       status=429,
                       headers={'X-Ratelimit-Usage': 11,
                                'X-Ratelimit-Limit': 10})
                    #    body=json.dumps([]).encode('utf-8'),
                    #    request=req)
        
        status_pre = self._get_spider_status()
        
        # Test that response passes through MW unaffected
        assert self.mw.process_response(req, res, self.spider) is res

        status_post = self._get_spider_status()

        # Test that MW sets a spider attribute
        assert status_pre is None
        assert status_post == 'active'

    def test_resp_not_limited(self):
        req = Request('http://example.com')
        res = Response('http://example.com', status=400)
        
        assert self._get_spider_status() is None

        # Test that response passes through MW unaffected
        assert self.mw.process_response(req, res, self.spider) is res

        assert self._get_spider_status() is None

    def test_req_limited(self):
        req = Request('http://example.com')
        self.spider.rate_limit_status = 'active'
        self.assertRaises(IgnoreRequest, 
                          self.mw.process_request, req, self.spider)

    def test_req_not_limited(self):
        req = Request('http://example.com')

        # Test that request passes through MW unaffected
        assert self.mw.process_request(req, self.spider) is None
