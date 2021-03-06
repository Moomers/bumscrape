# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import re
import store
from scrapy.exceptions import DropItem
from scrapy.conf import settings

class ValidateListing(object):
    def __init__(self):
        """defines whitelists, REs et al to validate the listing"""
        self.wanted_url_re = re.compile(r".*/wan/|.*/clt/")
        self.wanted_titles = ['want', 'looking for', 'looking 4', 'requested', 'need']
        self.topical_titles = ['bm', 'burning man']

    def process_item(self, item, spider):
        if spider.name == 'craigslist':
            return self.validate_cl_listing(item)
        else:
            return item

    def validate_cl_listing(self, item):
        ## exclude based on the url of the listing
        if self.wanted_url_re.match(item['url']):
            raise DropItem("URL looks like it's from a wanted subforum: %s" % item['url'])

        l_title = item['title'].lower()

        ## exclude if the title looks like a wanted ad
        if any(wanted_phrase in l_title
               for wanted_phrase in self.wanted_titles):
            raise DropItem("Title looks like a wanted listing: %s" % item['title'])

        ## skip results that aren't about burning man.
        if not any(bm_topic in l_title
                   for bm_topic in self.topical_titles):
            raise DropItem("Title doesn't look like it's about burning man: %s" % item['title'])

        return item

class StoreListing(object):
    def __init__(self):
        self.store = store.Store(settings)

    def open_spider(self, spider):
        self.store.connect()
        self.store.create_db()
        self.store.log_crawl(spider.name)

    def close_spider(self, spider):
        self.store.disconnect()

    def process_item(self, item, spider):
        """stores the listing into the db"""
        self.store.add_item(item, spider.name)
