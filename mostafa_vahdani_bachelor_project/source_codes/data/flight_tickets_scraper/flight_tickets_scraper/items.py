# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

# Items act as simple temporary containers to store the extracted data before further processing or saving it.

class FlightTicketsScraperItem(Item):
    ticket_id = Field()
    
    # going out of source airport
    national_departure_code = Field()

    # coming into the destination airport
    national_arrival_code = Field()

    arrival_city_name_persian = Field()
    departure_city_name_persian = Field()
    
    departure_time = Field()
    arrival_time = Field()
    departure_date = Field()
    departure_date_YMD_format = Field()

    company_name = Field()
    capacity = Field()
    flying_number = Field()
    flying_class = Field()
    ticket_price_T = Field()
    flying_type = Field()

    def set_all_default_value(self, value=None):
        for keys, _ in self.fields.items():
            self[keys] = value
