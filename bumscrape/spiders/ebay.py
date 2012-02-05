#!/usr/bin/env python

import json
import re
import urllib

from scrapy.spider import BaseSpider
from scrapy.http import Request
from bumscrape.items import BumscrapeItem

def get_query_url(endpoint, parameters):
    return endpoint + "?" + urllib.urlencode(parameters)

class EbayScraper(BaseSpider):
    name = "ebay"

    pageing = False
    endpoint = "http://svcs.ebay.com/services/search/FindingService/v1"
    parameters = {
            'OPERATION-NAME':'findItemsAdvanced',
            'SERVICE-VERSION':'1.11.0',
            'SECURITY-APPNAME':'Moomersda-68ea-4fc0-88f7-a53b23426ae',
            'RESPONSE-DATA-FORMAT':'JSON',
            'REST-PAYLOAD':'1',
            'keywords':'burning man',
            'categoryId':1305,
            'paginationInput.entriesPerPage':100,
            'paginationInput.pageNumber':1,
            }

    start_urls = [get_query_url(endpoint, parameters)]

    def parse(self, http_response):
        data = json.loads(http_response.body)['findItemsAdvancedResponse'][0]

        pagecount = int(data['paginationOutput'][0]['totalPages'][0])
        if not self.pageing and pagecount > 1:
            self.log("*** Going to make %s additional requests" % (pagecount,))

            self.pageing = True
            for pagenum in xrange(2, pagecount + 1):
                self.parameters['paginationInput.pageNumber'] = pagenum
                yield Request(get_query_url(self.endpoint, self.parameters), callback=self.parse)

        for item in data['searchResult'][0]['item']:
            yield BumscrapeItem(url=item['viewItemURL'][0],
                                title=item['title'][0],
                                price=item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                                #bids=item[0]['bidCount'],
                                #created=item[0]['listingInfo'][0]['startTime'],
                                #num_tickets=1, #correct number might be in an aspect...
                                )
