import logging
import json
import urllib.error
import urllib.request
from urllib.parse import urlencode
import psycopg2
import environ
from connect_db import ConnectDB
from create_table import ExchangeCurrency


root = environ.Path(__file__)
env = environ.Env()
environ.Env.read_env()
ConnectDB.set_connection()


logger = logging.getLogger('urllib')

logging.basicConfig(level=logging.DEBUG, format='%(process)d-%(levelname)s-%(message)s')


exchanger = ExchangeCurrency()
exchanger.create_table()


class ParserExchange():
    app_id = env.str("APP_ID")
    static_url = "https://openexchangerates.org/api/latest.json/"
    param = urlencode({'app_id': app_id})

    full_url = static_url + "?" + param

    def __init__(self, static_url=static_url, app_id=app_id, full_url=full_url, response=None):
        self.static_url = static_url
        self.app_id = app_id
        self.full_url = full_url
        self.url_request = urllib.request.Request(self.full_url)
        self.response = urllib.request.urlopen
        logger.info((self.url_request, self.url_request.get_method()))

    def catch_network_errors(self):
        try:

            self.response(self.url_request)

        except urllib.error.URLError as e:
            logger.error(e)

            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            raise
        else:
            return True

    def save_currency_to_db(self):

        try:
            if self.catch_network_errors() is True:
                data = json.load(self.response(self.url_request))
                for key, value in data.items():
                    if key == 'base':
                        exchanger.from_currency = value
                    elif key == 'rates':
                        data = data['rates'].items()
                        for key, value in data:
                            exchanger.to_currency = key
                            exchanger.rates_currency = value
                            exchanger.save()

        except psycopg2.errors.UniqueViolation as err:
            print(f'Value already exists {err}')
