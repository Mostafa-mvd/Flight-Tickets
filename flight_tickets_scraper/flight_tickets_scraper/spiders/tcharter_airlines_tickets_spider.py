from flight_tickets_scraper.items import FlightTicketsScraperItem

from flight_tickets_scraper.utils import (
    make_two_combinations_airports, 
    merge_two_lists, 
    list_odd_values, 
    list_even_values)

from random import shuffle
from time import sleep

import scrapy
import json


class AirlinesTickets(scrapy.Spider):
    name = "airlines_tickets"
    allowed_domains = ["www.tcharter.ir"]

    page_number = 1
    base_url = "https://www.tcharter.ir"
    request_method = "POST"
    request_payload = {
        "types": ["all", "system", "provider", "bclass", "economy"],
        "tab": "airplane",
    }

    def start_requests(self):
        """send request for every possible combination of two city airports."""

        combinations_result = make_two_combinations_airports()

        # TODO: shuffle result is just for test
        # shuffle(result)
        
        self.request_payload["selected_date"] = ""

        # TODO: combinations_result[:100] is just for test
        for source, destination in list(combinations_result)[:1]:
            meta = {
                "source_city": source,
                "destination_city": destination
            }

            # this section counter goes to number 4 because in tcharter js goes to number 4 for ticket calender page (show_calendar_page js function) in otherwise It will be out next page in calender page.
            for section_counter in range(1, 5):
                url = f"{self.base_url}/tickets/dates/{source}-{destination}-airplane?section={section_counter}"

                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    method=self.request_method,
                    body=json.dumps(self.request_payload),
                    meta=meta)
                
        self.request_payload.pop("selected_date")

    def parse(self, response, **kwargs):
        """first level of parsing for gathering tickets selling dates."""

        city_airline_date_codes = response.css(".daterow::attr(data)").extract()
        
        # if not then there is no airplane for selling its tickets, otherwise airplane date calender page is empty.
        if city_airline_date_codes:
            source_city = response.meta["source_city"]
            destination_city = response.meta["destination_city"]

            date_values = response.css("#dateItem > span:nth-child(1)::text").getall()
            datetime_values = list_odd_values(date_values)
            day_values = list_even_values(date_values)
            striped_day_values = map(str.strip, day_values)
            merged_dates = merge_two_lists(striped_day_values, datetime_values)
            
            for merged_date, city_airline_date_code in zip(merged_dates, city_airline_date_codes):
                url = f"{self.base_url}/tickets/tickets/{city_airline_date_code}/?airplane=&page=1"

                # TODO: this is just for test
                # self.parse_counter += 1
                
                cb_kwargs = {
                    "city_airline_date_code": city_airline_date_code,
                }

                meta = {
                    "date": merged_date,
                    "source_city": source_city,
                    "destination_city": destination_city,
                }

                yield scrapy.FormRequest(
                    url=url,
                    callback=self.parse_tickets_details,
                    method=self.request_method,
                    formdata=self.request_payload,
                    cb_kwargs=cb_kwargs,
                    meta=meta)

    def parse_tickets_details(self, response, **kwargs):
        """second level of parsing for gathering tickets information."""

        # TODO: check condition for pages navigation
        if response.body == b"error":
            self.page_number = 1
            return None

        tickets_table = response.css('table.main-ticket-list tbody')
        ticket_detail_trs = tickets_table.css("tr")
        
        # if not then there is no selling tickets for the day we want.
        if ticket_detail_trs:
            flight_ticket_item = FlightTicketsScraperItem()

            for ticket_detail_tr in ticket_detail_trs:
                ticket_detail_tds = ticket_detail_tr.css("td")

                flight_ticket_item["company_name"] = ticket_detail_tds[0].css("::attr(data-hint)").get()
                flight_ticket_item["arrival_time"] = ticket_detail_tds[1].css("::text").get()
                flight_ticket_item["capacity"] = ticket_detail_tds[2].css("::text").get()
                flight_ticket_item["flying_number"] = ticket_detail_tds[3].css("::text").get()
                flight_ticket_item["flying_class"] = ticket_detail_tds[4].css("::text").get()
                flight_ticket_item["ticket_price"] = ticket_detail_tds[6].css("::text").getall()[1].strip() + " T"
                flight_ticket_item["flying_type"] = ticket_detail_tds[7].css("::text").getall()[1].strip()

                flight_ticket_item["source"] = response.meta["source_city"]
                flight_ticket_item["destination"] = response.meta["destination_city"]
                flight_ticket_item["date"] = response.meta["date"]

                yield flight_ticket_item

            self.page_number += 1
            
            shared_city_airline_date_code = kwargs["city_airline_date_code"]

            next_page_url = f"{self.base_url}/tickets/tickets/{shared_city_airline_date_code}/?airplane&page={self.page_number}"
            
            cb_kwargs = {
                "shared_city_airline_date_code": shared_city_airline_date_code,
            }
            
            yield response.follow(
                url=next_page_url,
                callback=self.parse_tickets_details,
                method=self.request_method,
                body=json.dumps(self.request_payload),
                cb_kwargs=cb_kwargs)
