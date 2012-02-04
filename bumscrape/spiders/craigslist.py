#!/usr/bin/env python

import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

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

    # These urls are people looking for tickets, or 
    wanted_url_re = re.compile(r".*/wan/|.*/clt/|.*/clo/")

    # these strings inside the title indicate looking for tickets
    wanted_titles = ['want', 'looking for', 'looking 4', 'requested', 'need']

    # these strings in the title mean the post is about burning man
    topical_titles = ['bm', 'burning man']

    def parse_result(self, result):
        """Parses a single result"""
        def get_string(xpath):
            return ''.join(result.select(xpath).extract()).strip()

        url = get_string("a/@href")
        title = get_string("a/text()")
        match_price = self.price_re.search(get_string("text()"))
        price = match_price.groups(1)[0] if match_price else None

        return title, url, price

    def parse(self, response):
        """Parses a list of results"""
        hxs = HtmlXPathSelector(response)
        results = hxs.select("//p[@class = 'row']")

        for result in results:
            scalper = True

            title, url, price = self.parse_result(result)

            # exclude WANTED listings
            if (self.wanted_url_re.match(url) or
                any(wanted_phrase in title.lower()
                    for wanted_phrase in self.wanted_titles)): 
                continue

            # skip results that aren't about burning man.
            if not any(bm_topic in title.lower()
                       for bm_topic in self.topical_titles):
                continue

            # if we got here, this is probably a scalper.
            print title, url, price
