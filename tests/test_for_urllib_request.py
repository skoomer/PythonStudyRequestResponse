from unittest.case import TestCase
import urllib
import urllib.error
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlencode
import environ
import pytest
from connect_db import ConnectDB
from create_table import ExchangeCurrency
from pythonrequestsresponse.impl_urlib_requests import ParserExchange

root = environ.Path(__file__)
env = environ.Env()
environ.Env.read_env()

ConnectDB.set_connection()


class TestUrllibRequest(TestCase):
    def setUp(self):
        self.url = "https://openexchangerates.org/api/latest.json/"
        self.cursor = ConnectDB._get_cursor()
        self.parser = ParserExchange()
        self.exchanger = ExchangeCurrency()

    def test_urllib_request_200(self):
        self.assertEqual(self.parser.response(self.parser.full_url).getcode(), 200)

    def test_urllib_request_403(self):
        try:
            self.parser.response(self.url)
        except urllib.error.HTTPError as er:
            self.assertEqual(er.getcode(), 403)

    def test_catch_HTTPError(self):
        self.parser.url_request = "https://openexchangerates.org/api/latest.jsodadwn/"

        with pytest.raises(HTTPError) as er:
            self.parser.valid_response()
        self.assertEqual("HTTP Error 405: Method Not Allowed", str(er.value))

    def test_HTTPError_404(self):
        app_id = env.str("APP_ID")
        static_url = "https://openexchangerates.org/hello/api/latest.json"
        param = urlencode({'app_id': app_id})
        full_url = static_url + "?" + param
        self.parser.full_url = full_url
        self.parser.url_request = urllib.request.Request(self.parser.full_url)

        with pytest.raises(HTTPError)as er:
            self.parser.valid_response()

        self.assertEqual("<ExceptionInfo <HTTPError 404: 'Not Found'> tblen=8>", str(er))

    def test_valid_response_return_true(self):
        self.assertEqual(self.parser.valid_response(), True)

    def test_save_to_db(self):
        self.exchanger.create_table()
        self.parser.valid_response()
        self.parser.save_currency_to_db()
        query = "SELECT count(*) FROM exchangecurrency;"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (169,))

    def tearDown(self):
        drop = "DROP TABLE IF EXISTS exchangecurrency;"
        self.cursor.execute(drop)
