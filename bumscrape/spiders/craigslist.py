#!/usr/bin/env python

import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

def get_search_url(subdomain, query):
    return ("http://%s.craigslist.org/search?" +
        "areaID=1&subAreaID=&query=%s&catAbb=sss") % (
            subdomain, query.replace(" ", "+"))

class CraigslistSpider(BaseSpider):
    """Crawls craigslist to find scalped burning man tickets."""
    name = "craigslist"
    allowed_domains = "craigslist.org"
    subdomains = [
        "sfbay",
        "portland",
    ]
    queries = [
        "burning man tickets",
    ]
    start_urls = [get_search_url(subdomain, query)
                  for subdomain in subdomains
                  for query in queries]

    # Matches a price with a dollar sign in front.
    price_re = re.compile(r"\$(\d+(?:\.\d+)?)")

    # These urls are legit (people who want tickets etc.).
    whitelist_re = re.compile(r".*/wan/|.*/clt/")

    def parse_result(self, result):
       """Parses a single result"""
        def get_string(xpath):
            return ''.join(result.select(xpath).extract()).strip()
        url = get_string("a/@href")
        title = get_string("a/text()")
        match_price = CraigslistSpider.price_re.search(get_string("text()"))
        price = match_price.groups(1)[0] if match_price else None
        return title, url, price

    def parse(self, response):
       """Parses a list of results"""
        hxs = HtmlXPathSelector(response)
        results = hxs.select("//p[@class = 'row']")
        for result in results:
            title, url, price = self.parse_result(result)
            if CraigslistSpider.whitelist_re.match(url):
                # This is a legit listing.
                continue

            # This is probably a scalper.
            print title, url, price
