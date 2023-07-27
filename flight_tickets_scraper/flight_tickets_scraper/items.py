# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class FlightTicketsScraperItem(Item):
    source = Field()
    destination = Field()
    company_name = Field()
    arrival_time = Field()
    capacity = Field()
    flying_number = Field()
    flying_class = Field()
    ticket_price = Field()
    flying_type = Field()
    date = Field()
