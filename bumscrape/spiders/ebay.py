#!/usr/bin/env python

import json
import re
import urllib

from scrapy.spider import BaseSpider
from bumscrape.items import BumscrapeItem

def get_query_url(endpoint, parameters):
    return endpoint + "?" + urllib.urlencode(parameters)

class EbayScraper(BaseSpider):
    name = "ebay"

    endpoint = "http://svcs.ebay.com/services/search/FindingService/v1"
    parameters = {
            'OPERATION-NAME':'findItemsAdvanced',
            'SERVICE-VERSION':'1.11.0',
            'SECURITY-APPNAME':'Moomersda-68ea-4fc0-88f7-a53b23426ae',
            'RESPONSE-DATA-FORMAT':'JSON',
            'REST-PAYLOAD':'1',
            'keywords':'burning man',
            'categoryId':1305,
            }

    start_urls = [get_query_url(endpoint, parameters)]

    def parse(self, http_response):
        data = json.loads(http_response.body)
        print data
