from flight_tickets_scraper.utils import (
    two_permutation_airports_codes,
    filter_selectors,
)

from flight_tickets_scraper.items import FlightTicketsScraperItem

import scrapy
import json


class AirlinesTickets(scrapy.Spider):
    name = "airlines_tickets"
    allowed_domains = ["www.tcharter.ir"]

    request_method = "POST"
    base_url = "https://www.tcharter.ir"
    curl_request_raw_payload = r'types=%5B%22all%22%2C%22system%22%2C%22provider%22%2C%22bclass%22%2C%22economy%22%5D&tab=airplane'

    item_id = 1

    def start_requests(self):
        """send request for every possible permutation of two city airports."""

        two_permutation_result = list(two_permutation_airports_codes())

        for source, destination in two_permutation_result[:2]:
            cb_kwargs = {
                "source_city": source,
                "destination_city": destination
            }

            url = f"{self.base_url}//tickets/search/0/{source}-{destination}"

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                method=self.request_method,
                body=self.curl_request_raw_payload,
                cb_kwargs=cb_kwargs)

    def parse(self, response, **kwargs):
        """first level of parsing for gathering airplanes dates sections urls."""

        airplane_dates_table = response.css(".ftmini")

        if airplane_dates_table:

            request_payload = {
                "types": ["all", "system", "provider", "bclass", "economy"],
                "tab": "airplane",
                "selected_date": "",
            }

            source = response.cb_kwargs["source_city"]
            destination = response.cb_kwargs["destination_city"]

            # this section counter goes to number 4 because in tcharter js goes to number 4 for ticket calender table (show_calendar_page js function) in otherwise It will be out next page in calender page.
            for section_counter in range(1, 5):
                url = f"{self.base_url}/tickets/dates/{source}-{destination}-airplane?section={section_counter}"

                yield scrapy.Request(
                    url=url,
                    callback=self.parse_airplane_dates_table,
                    method=self.request_method,
                    body=json.dumps(request_payload),
                    cb_kwargs=response.cb_kwargs)

    def parse_airplane_dates_table(self, response, **kwargs):
        """second level of parsing for gathering tickets selling dates."""

        city_airline_date_rows = response.css(".daterow")
        filtered_city_airline_rows = filter_selectors(city_airline_date_rows, ".currency_symbole")
            
        for filtered_city_airline_row in filtered_city_airline_rows:
            city_airline_date_code = filtered_city_airline_row.css(".daterow::attr(data)").get()
            date_values = filtered_city_airline_row.css("#dateItem > span:nth-child(1)::text").getall()

            url = f"{self.base_url}/tickets/tickets/{city_airline_date_code}/"

            response.cb_kwargs["city_airline_date_code"] = city_airline_date_code
            response.cb_kwargs["date"] = f"{date_values[0].strip()} {date_values[1]}"
            response.cb_kwargs["page_number"] = 1

            yield scrapy.Request(
                url=url,
                callback=self.parse_tickets_table,
                method=self.request_method,
                body=self.curl_request_raw_payload,
                cb_kwargs=response.cb_kwargs)

    def parse_tickets_table(self, response, **kwargs):
        """third level of parsing for gathering tickets information."""

        if response.body == b"error":
            return None

        tickets_table = response.css('.table.main-ticket-list tbody')
        ticket_detail_trs = tickets_table.css(".airplane-row")
        ticket_detail_blue_tr = tickets_table.css(".blue-light")

        if ticket_detail_blue_tr:
            ticket_detail_trs += ticket_detail_blue_tr
        
        # if not then there is no selling tickets for the day we want.
        if ticket_detail_trs:
            for ticket_detail_tr in ticket_detail_trs:
                flight_ticket_item = FlightTicketsScraperItem()
                flight_ticket_item.set_all_default_value()

                ticket_detail_tds = ticket_detail_tr.css("td")

                flight_ticket_item["company_name"] = ticket_detail_tds[0].css("::attr(data-hint)").get()
                flight_ticket_item["departure_time"] = ticket_detail_tds[1].css("::text").get()
                flight_ticket_item["capacity"] = ticket_detail_tds[2].css("::text").get()
                flight_ticket_item["flying_number"] = ticket_detail_tds[3].css("::text").get()
                flight_ticket_item["flying_class"] = ticket_detail_tds[4].css("::text").get()
                flight_ticket_item["ticket_price_T"] = ticket_detail_tds[6].css("::text").getall()[1].strip()
                flight_ticket_item["flying_type"] = ticket_detail_tds[7].css("::text").getall()[1].strip()

                flight_ticket_item["national_departure_code"] = response.cb_kwargs["source_city"]
                flight_ticket_item["national_arrival_code"] = response.cb_kwargs["destination_city"]
                flight_ticket_item["departure_date"] = response.cb_kwargs["date"]

                flight_ticket_item["ticket_id"] = self.item_id
                self.item_id += 1

                ticket_extra_detail_url = ticket_detail_tds[7].css(".finishDescription a::attr(href)").get()

                if (flight_ticket_item["flying_type"] and 
                    'go' not in ticket_extra_detail_url.split("/")):

                        flight_ticket_item_cb_kwargs = {
                            "flight_ticket_item": flight_ticket_item
                        }

                        method = "GET"

                        yield scrapy.Request(
                            url=ticket_extra_detail_url,
                            callback=self.parse_extra_detail,
                            method=method,
                            cb_kwargs=flight_ticket_item_cb_kwargs)
                else:
                    yield flight_ticket_item

            #When parsed the all items in each page's tables comes here.
            response.cb_kwargs["page_number"] += 1
            next_page_number = response.cb_kwargs["page_number"]

            city_airline_date_code = response.cb_kwargs["city_airline_date_code"]

            next_page_url = f"{self.base_url}/tickets/tickets/{city_airline_date_code}?page={next_page_number}"
                
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_tickets_table,
                method=self.request_method,
                body=self.curl_request_raw_payload,
                cb_kwargs=response.cb_kwargs)

    def parse_extra_detail(self, response, **kwargs):
        """fourth level of parsing for gathering tickets detail."""

        flight_ticket_item = response.cb_kwargs["flight_ticket_item"]
        ticket_extra_detail = response.css(".ps-2 div::text").get().strip()
        splitted_detail = ticket_extra_detail.split()

        flight_ticket_item["arrival_time"] = splitted_detail[-3]
        flight_ticket_item["arrival_city_name_persian"] = splitted_detail[3]
        flight_ticket_item["departure_city_name_persian"] = splitted_detail[1]
        flight_ticket_item["departure_date_YMD_format"] = splitted_detail[6]

        yield flight_ticket_item
