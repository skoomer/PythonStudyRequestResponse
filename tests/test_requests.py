from unittest.case import TestCase
import unittest
from unittest import mock
import requests
import pytest
from requests.exceptions import Timeout, TooManyRedirects, HTTPError, ConnectionError
from pythonrequestsresponse.impl_requests import ParserExchange


class TestRequests(TestCase):
    def setUp(self):
        self.parser = ParserExchange()
        self.url = "https://openexchangerates.org/api/latest.json/"

    def test_catch_HTTPError(self):
        self.parser.url_request.raise_for_status = mock.Mock(requests.get, side_effect=HTTPError)

        requests.get.return_value = self.parser.url_request

        with pytest.raises(HTTPError)as er:
            self.parser.catch_network_errors()

        self.assertEqual('<ExceptionInfo HTTPError() tblen=5>', str(er))

    def test_catch_ConnectionError_error(self):

        self.parser.url_request.raise_for_status = mock.Mock(requests.get, side_effect=ConnectionError)
        requests.get.return_value = self.parser.url_request

        with pytest.raises(ConnectionError)as er:
            self.parser.catch_network_errors()

        self.assertEqual('<ExceptionInfo ConnectionError() tblen=5>', str(er))

    def test_catch_TooManyRedirects_error(self):

        self.parser.url_request.raise_for_status = mock.Mock(requests.get, side_effect=TooManyRedirects)
        requests.get.return_value = self.parser.url_request

        with pytest.raises(TooManyRedirects)as er:
            self.parser.catch_network_errors()

        self.assertEqual('<ExceptionInfo TooManyRedirects() tblen=5>', str(er))

    def test_catch_Timeout_error(self):

        self.parser.url_request.raise_for_status = mock.Mock(requests.get, side_effect=Timeout)
        requests.get.return_value = self.parser.url_request

        with pytest.raises(Timeout)as er:
            self.parser.catch_network_errors()

        self.assertEqual('<ExceptionInfo Timeout() tblen=5>', str(er))


if __name__ == '__main__':
    unittest.main()
