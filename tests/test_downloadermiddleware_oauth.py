"""
Based on:
https://github.com/scrapy/scrapy/blob/2.8.0/tests/test_downloadermiddleware_httpauth.py
"""
import unittest

from oauthlib.oauth2.rfc6749.errors import InsecureTransportError
from scrapy.http import Request
from scrapy.spiders import Spider

from scrapy_strava.middlewares.oauth import StravaOAuth2Middleware


class TestSpider(Spider):
    oauth_client_id = 12345
    oauth_access_token = 'access_token'
    # http_oauth_domain = 'example.com'


class OAuth2MiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.mw = StravaOAuth2Middleware()
        self.spider = TestSpider('foo')
        self.mw.spider_opened(self.spider)

    def tearDown(self):
        del self.mw

    def test_auth_domain(self):
        req = Request('https://example.com/')
        req2 = self.mw.process_request(req, self.spider)
        self.assertIsInstance(req2, Request)
        self.assertIsNot(req, req2)
        self.assertEqual(req2.headers['Authorization'], b'Bearer access_token')

    def test_auth_subdomain(self):
        req = Request('https://foo.example.com/')
        req2 = self.mw.process_request(req, self.spider)
        assert isinstance(req2, Request)
        assert req is not req2
        self.assertEqual(req2.headers['Authorization'], b'Bearer access_token')

    def test_auth_already_set(self):
        req = Request('https://example.com/', 
                      headers=dict(Authorization='Bearer access_token'),
                      meta=dict(oauth=True))
        self.assertIsNone(self.mw.process_request(req, self.spider))
        self.assertEqual(req.headers['Authorization'], b'Bearer access_token')

    def test_no_https(self):
        req = Request('http://example.com/')
        self.assertRaises(InsecureTransportError, 
                          self.mw.process_request, req, self.spider)

    # def test_no_auth(self):
    #     req = Request('https://example-noauth.com/')
    #     assert self.mw.process_request(req, self.spider) is None
    #     self.assertNotIn('Authorization', req.headers)
