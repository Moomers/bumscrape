# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BumscrapeItem(Item):
    """A web page offering scalped tickets."""
    url = Field()  # The url of the page.
    title = Field()  # The html title of the page.
    num_tickets = Field()  # The number of tickets for sale.
    price = Field()  # The price of the tickets.
