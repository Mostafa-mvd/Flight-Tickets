from itertools import combinations
from json import load
from random import shuffle
from time import sleep

import json
import pathlib
import scrapy
import platform


class AirlinesTickets(scrapy.Spider):
    page_number = 1
    name = "airlines_tickets"
    base_url = "https://www.tcharter.ir"
    allowed_domains = [
        "www.tcharter.ir",
        ]

    def get_airports_codes(self):
        parent_path = pathlib.Path(__file__).parent.parent.parent.parent
        json_file_path = parent_path.joinpath("source", "airport_city_codes.json")
        json_file_handler = open(json_file_path)
        airports_city = load(json_file_handler)
        airports_codes = airports_city["CityCodes"]
        json_file_handler.close()

        return airports_codes

    def make_two_combination_airports(self):
        def check_equal_constraint(airports_codes):
            if (airports_codes[0], airports_codes[1]) != ("THR", "IKA"):
                return True

        airports_city_codes_lst = self.get_airports_codes()
        airports_codes_lst = [airport_city_code_dict["id"] for airport_city_code_dict in airports_city_codes_lst]
        two_combinations_codes = filter(check_equal_constraint, combinations(airports_codes_lst, 2))

        return two_combinations_codes

    def start_requests(self):
        """send request for every possible combination of two city airports."""

        urls = list()

        result = list(self.make_two_combination_airports())
        
        # TODO: shuffle result is just for test
        shuffle(result)
        
        payload = {
            "types": ["all", "system", "provider", "bclass", "economy"],
            "tab": "airplane",
            "selected_date": "",
        }

        method = "POST"

        # TODO: result[:100] is just for test
        for origin, destination in result[:100]:
            # this section counter goes to number 4 because in tcharter js goes to number 4 for ticket calender page (show_calendar_page js function).
            # it will be out next page in calender page.
            for section_counter in range(1, 5):
                # For Example: https://www.tcharter.ir/tickets/dates/MHD-THR-airplane?section=1
                url = f"{self.base_url}/tickets/dates/{origin}-{destination}-airplane?section={section_counter}"
                urls.append(url)

        # len(result) = 2015
        # len(result) * 4 = len(urls) = 8060
        for url in urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse, 
                method=method, 
                body=json.dumps(payload))

    def parse(self, response, **kwargs):
        """first level of parsing for gathering tickets selling dates."""

        city_airline_date_codes = response.css(".daterow::attr(data)").extract()

        payload = {
            "tab": "airplane",
        }

        method = "POST"

        urls = list()
        
        # if not then there is no airplane for selling its tickets
        # airplane date calender page is empty
        if city_airline_date_codes:
            for city_airline_date_code in city_airline_date_codes:
                # For Example: https://www.tcharter.ir/tickets/tickets/TUhELVRIUi0xNDAyLzA1LzAz/?airplane&page=1
                url = f"{self.base_url}/tickets/tickets/{city_airline_date_code}/?airplane="
                urls.append(url)

            for url, city_airline_date_code in zip(urls, city_airline_date_codes):
                cb_kwargs = {
                    "shared_city_airline_date_code": city_airline_date_code,
                }

                yield scrapy.Request(
                    url=url, 
                    callback=self.parse_tickets_details,
                    method=method, 
                    body=json.dumps(payload),
                    cb_kwargs=cb_kwargs)

    def parse_tickets_details(self, response, shared_city_airline_date_code):
        """second level of parsing for gathering tickets information."""

        if not response:
            self.page_number = 1
            return None

        #get trs of selling table
        selling_tickets_rows = response.css(".airplane-row")
        
        if selling_tickets_rows:
            for selling_ticket_row in selling_tickets_rows:
                # TODO: extract data from each tds and store them in csv with pipelines.
                tickets_tds = selling_ticket_row.css("td")

            self.page_number += 1
            url = f"{self.base_url}/tickets/tickets/{shared_city_airline_date_code}/?airplane&page={self.page_number}"
            payload = {
                "tab": "airplane",
            }
            cb_kwargs = {
                "shared_city_airline_date_code": shared_city_airline_date_code,
            }
            method = "POST"

            yield scrapy.Request(
                url=url,
                callback=self.parse_tickets_details,
                method=method,
                body=json.dumps(payload),
                cb_kwargs=cb_kwargs)
