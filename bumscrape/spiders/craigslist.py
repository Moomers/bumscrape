#!/usr/bin/env python

import datetime
import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from bumscrape.items import BumscrapeItem

def get_search_url(subdomain, query):
    return ("http://%s.craigslist.org/search?" +
            "areaID=1&subAreaID=&query=%s&catAbb=sss") % (
                    subdomain, query.replace(" ", "+"))

subdomains_file = "bumscrape/spiders/data/craigslist_test_subdomains"

class CraigslistSpider(BaseSpider):
    """Crawls craigslist to find scalped burning man tickets."""
    name = "craigslist"
    allowed_domains = "craigslist.org"
    subdomains = [line.strip() for line in file(subdomains_file).readlines()]
    queries = [
        "burning man tickets",
    ]
    start_urls = [get_search_url(subdomain, query)
                  for subdomain in subdomains
                  for query in queries]

    # Matches a price with a dollar sign in front.
    price_re = re.compile(r"\$(\d+(?:\.\d+)?)")

    # Matches a craigslist posting date.
    # We just grab the approximate post date from the search result page,
    # because it's not worth it to crawl the result page just for a date.
    date_re = re.compile(
        r"^((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+)")

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
        results = hxs.select("//p[@class = 'row']")

        for result in results:
            title, url, price, posted = self.parse_result(result)
            yield BumscrapeItem(title=title,
                                url=url,
                                price=price,
                                posted=posted)
