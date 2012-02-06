# Scrapy settings for bumscrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'bumscrape'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['bumscrape.spiders']
NEWSPIDER_MODULE = 'bumscrape.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
        'bumscrape.pipelines.ValidateListing',
        'bumscrape.pipelines.StoreListing',
]

MYSQL_HOST = 'localhost'
MYSQL_USER = 'bumscrape'
MYSQL_PASSWD = 'bumscrape'
MYSQL_DB = 'bumscrape'
