# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

# If you need additional processing of the extracted data before saving it, you can use Scrapy pipelines. Pipelines allow you to perform tasks like data validation, cleaning, or saving to a database.

class FlightTicketsScraperPipeline:
    def process_item(self, item, spider):
        return item

class TicketArrivalTimePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        arrival_time = adapter.get("arrival_time")

        if arrival_time:
            splitted_arrival_time = arrival_time.split(":")

            if splitted_arrival_time[0] == "ورود":
                item["arrival_time"] = None

        return item

class DuplicatesItemsPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["ticket_id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found:\n")
        else:
            self.ids_seen.add(adapter["ticket_id"])
            return item
