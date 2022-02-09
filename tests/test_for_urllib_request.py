from unittest.case import TestCase
import urllib
import urllib.error
import urllib.request
import pytest
from pythonrequestsresponse.impl_urlib_requests import ParserExchange


class TestUrllibRequest(TestCase):
    def setUp(self):
        self.url = "https://openexchangerates.org/api/latest.json/"

        self.parser = ParserExchange()

    def test_urllib_request_200(self):
        self.assertEqual(self.parser.response(self.parser.full_url).getcode(), 200)

    def test_urllib_request_403(self):
        try:
            self.parser.response(self.url)
        except urllib.error.HTTPError as er:
            self.assertEqual(er.getcode(), 403)

    def test_catch_HTTPError(self):
        self.parser.url_request = "https://openexchangerates.org/api/latest.jsodadwn/"

        with pytest.raises(urllib.error.HTTPError) as er:
            self.parser.catch_network_errors()
        self.assertEqual("HTTP Error 405: Method Not Allowed", str(er.value))
