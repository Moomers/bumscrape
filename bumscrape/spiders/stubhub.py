#!/usr/bin/env python

import json
import re
import urllib

from scrapy.spider import BaseSpider
from bumscrape.items import BumscrapeItem

def get_query_url(endpoint, query, fields):
    return endpoint + "?" + urllib.urlencode(
        {"q": query,
         "version": "2.2",
         "start": "0",
         "indent": "on",
         "wt": "json",
         "fl": " ".join(fields)})

def get_ticket_url(ticket_id):
    return ("http://www.stubhub.com/burning-man-festival-tickets" +
            "/burning-man-8-27-2012-4016620/?ticket_id=" + ticket_id)

class StubhubScraper(BaseSpider):
    name = "stubhub"
    endpoint = "http://publicfeed.stubhub.com/listingCatalog/select/"
    solr_query = "+stubhubDocumentType:ticket +event_id:4016620"
    query_fields = ["stubhubDocumentId", "curr_price", "quantity"]
    start_urls = [get_query_url(endpoint, solr_query, query_fields)]
    ticket_re = re.compile(r"^ticket-(\d+)$")

    def parse(self, http_response):
        data = json.loads(http_response.body)
        response = data.get('response', {})
        ticket_batches = response.get('docs', [])
        for batch in ticket_batches:
            if not all(field in batch for field in self.query_fields):
                # This batch is missing some required data field.
                continue
            # Get id from a ticket id string like "ticket-434128915".
            # We need this to make a url for indexing.
            match = self.ticket_re.match(batch['stubhubDocumentId'])
            if not match:
                continue
            ticket_id = match.groups(1)[0]
            yield BumscrapeItem(url=get_ticket_url(ticket_id),
                                price=batch['curr_price'],
                                num_tickets=batch['quantity'])
