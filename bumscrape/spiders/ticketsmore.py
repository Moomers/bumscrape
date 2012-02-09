#!/usr/bin/env python

import datetime
import re

from scrapy.spider import BaseSpider
from scrapy.http import Request

from bumscrape.items import BumscrapeItem

class TicketsmoreSpider(BaseSpider):
    """Crawls results for Ticketsmore ticket-selling site"""
    name = "ticketsmore"
    allowed_domains = ["ticketsmore.com", "tickettransaction.com"]

    event_id = "1795197"
    start_urls = ["""http://www.ticketsmore.com/ResultsTicket.php?evtid=%s&event=Burning+Man+2012""" % event_id]

    script_re = re.compile('<script.*?>(.*?)</script>', re.MULTILINE | re.DOTALL)
    js_url_re = re.compile("""src=['"]([^'"]+)""")
    ticket_re = re.compile("""">(.*?)<"\+""")

    def make_url(self, identifier):
        return "https://secure.ticketsmore.com/checkout/Checkout.aspx?e=%s" % identifier

    def parse(self, response):
        """Parses the initial page, which only contains the javascript to the real tickets

        We extract the js url and parse that separetely
        """
        for m in self.script_re.finditer(response.body):
            script = m.group(1)
            if 'tickettransaction' in script:
                n = self.js_url_re.search(script)
                if n:
                    url = n.group(1).rstrip('/')
                    if not url.endswith('&'):
                        url += '&'
                    url += 'evtid=%s' % self.event_id

                    print url
                    yield Request(url, callback=self.parse_javascript)

    def parse_javascript(self, response):
        """Parses javascript from tickettransaction to find actual ticket listings"""
        for m in self.ticket_re.finditer(response.body):
            parts = m.group(1).split('>')

            part_names = {
                    0:'title',
                    1:'section',
                    2:'num_tickets',
                    3:'price',
                    6:'identifier'}

            ticket = {}
            for index, key in part_names.items():
                ticket[key] = parts[index]
            ticket['url'] = self.make_url(ticket['identifier'])

            yield BumscrapeItem(
                    url = ticket['url'],
                    title = ticket['title'],
                    num_tickets = ticket['num_tickets'],
                    price = ticket['price'],
                    )
