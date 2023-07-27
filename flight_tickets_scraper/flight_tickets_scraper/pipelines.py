# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# If you need additional processing of the extracted data before saving it, you can use Scrapy pipelines. Pipelines allow you to perform tasks like data validation, cleaning, or saving to a database.

class FlightTicketsScraperPipeline:
    def process_item(self, item, spider):
        return item
