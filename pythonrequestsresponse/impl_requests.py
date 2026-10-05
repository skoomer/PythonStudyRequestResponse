import logging
import requests
import psycopg2
import environ
from connect_db import ConnectDB


from create_table import ExchangeCurrency
root = environ.Path(__file__)
env = environ.Env()
environ.Env.read_env()
ConnectDB.set_connection()


logger = logging.getLogger('requests')
logging.basicConfig(level=logging.DEBUG)


exchanger = ExchangeCurrency()
exchanger.create_table()


class ParserExchange():
    app_id = env.str("APP_ID")
    static_url = "https://openexchangerates.org/api/latest.json/"

    def __init__(self, static_url=static_url, app_id=app_id):
        self.static_url = static_url
        self.app_id = app_id

        self.url_request = requests.get(static_url,
                                        params={'app_id': app_id})

    def catch_network_errors(self):
        try:
            response = self.url_request

            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            raise
        except requests.exceptions.ConnectionError as err:
            logger.error(err)
            raise
        except requests.exceptions.TooManyRedirects as err:
            logger.error(err)
            raise
        except requests.exceptions.Timeout as err:
            logger.error(err)
            raise
        else:
            return True

    def save_currency_to_db(self):
        try:
            if self.catch_network_errors() is True:
                for key, value in self.url_request.json().items():
                    if key == 'base':
                        exchanger.from_currency = value
                    elif key == 'rates':
                        data = self.url_request.json()['rates'].items()
                        for key, value in data:
                            exchanger.to_currency = key
                            exchanger.rates_currency = value
                            exchanger.save()

        except psycopg2.errors.UniqueViolation as err:
            print(f'Value already exists {err}')


pr = ParserExchange()
pr.save_currency_to_db()
