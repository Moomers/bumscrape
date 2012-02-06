#!/usr/bin/env python

import datetime
import json
import urllib

from scrapy.spider import BaseSpider
from scrapy.http import Request
from bumscrape.items import BumscrapeItem

def get_query_url(endpoint, parameters):
    """Simple function for generating URLs for the eBay API"""
    return endpoint + "?" + urllib.urlencode(parameters)

class EbayScraper(BaseSpider):
    """Scraper that finds BM tickets on eBay using the eBay API"""
    name = "ebay"

    endpoint = "http://svcs.ebay.com/services/search/FindingService/v1"
    parameters = {
            ## these parameters are required for the finding API
            'OPERATION-NAME':'findItemsAdvanced',
            'SERVICE-VERSION':'1.11.0',
            'SECURITY-APPNAME':'Moomersda-68ea-4fc0-88f7-a53b23426ae',
            'RESPONSE-DATA-FORMAT':'JSON',
            'REST-PAYLOAD':'1',

            ## these are arguments to the findItemsAdvanced call
            'keywords':'burning man',
            'categoryId':1305,                      #eBay category for 'tickets'
            'paginationInput.entriesPerPage':100,   #maximum number for items per page
            'paginationInput.pageNumber':1,         #start at page 1 by default
            }

    start_urls = [get_query_url(endpoint, parameters)]
    alreadyPaging = False

    def parse(self, http_response):
        """Parses a single API request, yielding items and additional pages to check"""
        data = json.loads(http_response.body)['findItemsAdvancedResponse'][0]

        if not self.alreadyPaging:
            self.alreadyPaging = True

            ## page through additional results if we have multiple pages
            pagecount = int(data['paginationOutput'][0]['totalPages'][0])
            if pagecount > 1:
                for pagenum in xrange(2, pagecount + 1):
                    self.parameters['paginationInput.pageNumber'] = pagenum
                    yield Request(get_query_url(self.endpoint, self.parameters), callback=self.parse)

        for item in data['searchResult'][0]['item']:
            try:
                posted = datetime.datetime.strptime(
                        item['listingInfo'][0]['startTime'][0],
                        "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                posted = None

            yield BumscrapeItem(url=item['viewItemURL'][0],
                                title=item['title'][0],
                                price=item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                                posted=posted
                                #bids=item[0]['bidCount'],
                                #num_tickets=1, #correct number might be in an aspect...
                                )
