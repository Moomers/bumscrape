# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import re
from scrapy.exceptions import DropItem

class ValidateListing(object):
    def __init__(self):
        """defines whitelists, REs et al to validate the listing"""
        self.wanted_url_re = re.compile(r".*/wan/|.*/clt/")
        self.wanted_titles = ['want', 'looking for', 'looking 4', 'requested', 'needed']

    def process_item(self, item, spider):
        if spider.name == 'craigslist':
            return self.validate_cl_listing(item)
        else:
            print "*** spider is %s" % spider.name
            return item

    def validate_cl_listings(self, item):
        #exclude based on the url of the listing
        if self.wanted_url_re.match(item['url']):
            raise DropItem("URL looks like it's from a wanted subforum: %s" % item['url'])

        #exclude based on stuff in the title
        l_title = item['title'].lower()
        for w_title in self.wanted_titles:
            if w_title in l_title:
                raise DropItem("Title looks like a wanted listing: %s" % item['title'])

        return item

class StoreListing(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        """stores the listing into the db"""
        print item
