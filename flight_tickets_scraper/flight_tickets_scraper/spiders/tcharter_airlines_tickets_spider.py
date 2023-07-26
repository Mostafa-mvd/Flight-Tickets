from flight_tickets_scraper.utils import make_two_combinations_airports
from random import shuffle
from time import sleep

import scrapy
import json


class AirlinesTickets(scrapy.Spider):
    name = "airlines_tickets"
    allowed_domains = ["www.tcharter.ir"]

    page_number = 1
    parse_counter = 0
    base_url = "https://www.tcharter.ir"
    request_method = "POST"
    request_payload = {
        "types": ["all", "system", "provider", "bclass", "economy"],
        "tab": "airplane",
    }

    def start_requests(self):
        """send request for every possible combination of two city airports."""

        result = make_two_combinations_airports()

        # TODO: shuffle result is just for test
        # shuffle(result)
        
        self.request_payload["selected_date"] = ""

        # TODO: result[:100] is just for test
        for origin, destination in list(result)[:1]:
            # this section counter goes to number 4 because in tcharter js goes to number 4 for ticket calender page (show_calendar_page js function) in otherwise It will be out next page in calender page.
            for section_counter in range(1, 5):
                url = f"{self.base_url}/tickets/dates/{origin}-{destination}-airplane?section={section_counter}"

                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    method=self.request_method,
                    body=json.dumps(self.request_payload))
                
        self.request_payload.pop("selected_date")

    def parse(self, response, **kwargs):
        """first level of parsing for gathering tickets selling dates."""

        city_airline_date_codes = response.css(".daterow::attr(data)").extract()
        
        # if not then there is no airplane for selling its tickets otherwise airplane date calender page is empty
        if city_airline_date_codes:
            for city_airline_date_code in city_airline_date_codes:
                url = f"{self.base_url}/tickets/tickets/{city_airline_date_code}/?airplane=&page=1"

                # TODO: this is just for test
                # self.parse_counter += 1
                
                cb_kwargs = {
                    "shared_city_airline_date_code": city_airline_date_code,
                }

                yield scrapy.FormRequest(
                    url=url,
                    callback=self.parse_tickets_details,
                    method=self.request_method,
                    formdata=self.request_payload,
                    cb_kwargs=cb_kwargs)

    def parse_tickets_details(self, response, **kwargs):
        """second level of parsing for gathering tickets information."""

        shared_city_airline_date_code = kwargs["shared_city_airline_date_code"]

        if response.body == b"error":
            self.page_number = 1
            return None

        tickets_table = response.css('.ticketList')
        ticket_detail_trs = tickets_table.css("tr")
        
        if ticket_detail_trs:
            for ticket_detail_tr in ticket_detail_trs:
                # TODO: extract data from each tds and store them in csv with pipelines.
                ticket_detail_tds = ticket_detail_tr.css("td")

            self.page_number += 1
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
