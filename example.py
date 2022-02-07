
import requests
import urllib, urllib.request, json
import urllib.parse
from urllib.parse import urlparse

base_url_api = "https://openexchangerates.org/api/"

base_url_api_endpoint = ["latest.json", "currencies.json","historical/2013-02-16.json"]


connect_url = "https://openexchangerates.org/api/latest.json?app_id=b8f18d7fa6db43569f7baf3761cc6abe"

res = requests.get(url=connect_url)


# print(res.json()['rates']['RUB'])


url = urllib.request.urlopen(connect_url)
data = json.loads(url.read().decode())
print(data)


