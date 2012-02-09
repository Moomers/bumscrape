#!/usr/bin/env python

import datetime
import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from bumscrape.items import BumscrapeItem

class TicketsmoreSpider(BaseSpider):
    """Crawls results for Ticketsmore ticket-selling site"""
    name = "ticketsmore"
    allowed_domains = "ticketsmore.com"

    start_urls = ["""http://www.ticketsmore.com/ResultsTicket.php?evtid=1795197&event=Burning+Man+2012"""]

    def parse_result(self, result):
        """Parses a single result"""
        def get_string(xpath):
            return ''.join(result.select(xpath).extract()).strip()

        url = get_string("a/@href")
        title = get_string("a/text()")
        text = get_string("text()")
        match_price = self.price_re.search(text)
        price = match_price.groups(1)[0] if match_price else None
        match_date = self.date_re.search(text)
        posted = None
        if match_date:
            date_string = match_date.groups(1)[0]
            posted = datetime.datetime.strptime(
                "%s 2012" % date_string, "%b %d %Y")

        return title, url, price, posted

    def parse(self, response):
        """Parses a list of results"""
        hxs = HtmlXPathSelector(response)
        results = hxs.select("div[@id = 'ssc_tktGroups']/div")

        for result in results:
            print result
            return

            title, url, price, posted = self.parse_result(result)
            yield BumscrapeItem(title=title,
                                url=url,
                                price=price,
                                posted=posted)
