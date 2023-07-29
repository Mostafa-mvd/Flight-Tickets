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

    def start_requests(self):
        """send request for every possible combination of two city airports."""

        combinations_result = two_permutation_airports_codes()

        for source, destination in combinations_result:
            meta = {
                "source_city": source,
                "destination_city": destination
            }

            url = f"{self.base_url}//tickets/search/0/{source}-{destination}"

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                method=self.request_method,
                body=self.curl_request_raw_payload,
                meta=meta)

    def parse(self, response, **kwargs):
        """first level of parsing for gathering airplanes dates sections urls."""

        airplane_dates_table = response.css(".ftmini")

        if airplane_dates_table:

            request_payload = {
                "types": ["all", "system", "provider", "bclass", "economy"],
                "tab": "airplane",
                "selected_date": "",
            }

            source = response.meta["source_city"]
            destination = response.meta["destination_city"]

            # this section counter goes to number 4 because in tcharter js goes to number 4 for ticket calender table (show_calendar_page js function) in otherwise It will be out next page in calender page.
            for section_counter in range(1, 5):
                url = f"{self.base_url}/tickets/dates/{source}-{destination}-airplane?section={section_counter}"

                yield scrapy.Request(
                    url=url,
                    callback=self.parse_airplane_dates_table,
                    method=self.request_method,
                    body=json.dumps(request_payload),
                    meta=response.meta)

    def parse_airplane_dates_table(self, response, **kwargs):
        """second level of parsing for gathering tickets selling dates."""

        city_airline_date_rows = response.css(".daterow")
        filtered_city_airline_rows = filter_selectors(city_airline_date_rows, ".currency_symbole")
            
        for filtered_city_airline_row in filtered_city_airline_rows:
            city_airline_date_code = filtered_city_airline_row.css(".daterow::attr(data)").get()
            date_values = filtered_city_airline_row.css("#dateItem > span:nth-child(1)::text").getall()

            url = f"{self.base_url}/tickets/tickets/{city_airline_date_code}/"
                
            cb_kwargs = {
                "city_airline_date_code": city_airline_date_code,
            }

            response.meta["date"] = f"{date_values[0].strip()} {date_values[1]}"
            response.meta["page_number"] = 1

            yield scrapy.Request(
                url=url,
                callback=self.parse_tickets_table,
                method=self.request_method,
                body=self.curl_request_raw_payload,
                cb_kwargs=cb_kwargs,
                meta=response.meta)

    def parse_tickets_table(self, response, **kwargs):
        """third level of parsing for gathering tickets information."""

        if response.body == b"error":
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
                flight_ticket_item["ticket_price"] = ticket_detail_tds[6].css("::text").getall()[1].strip()
                flight_ticket_item["flying_type"] = ticket_detail_tds[7].css("::text").getall()[1].strip()

                flight_ticket_item["source"] = response.meta["source_city"]
                flight_ticket_item["destination"] = response.meta["destination_city"]
                flight_ticket_item["date"] = response.meta["date"]

                yield flight_ticket_item

            #When parsed the all items in each page's tables comes here.
            response.meta["page_number"] += 1
            next_page_number = response.meta["page_number"]

            city_airline_date_code = kwargs["city_airline_date_code"]

            next_page_url = f"{self.base_url}/tickets/tickets/{city_airline_date_code}?page={next_page_number}"
                
            cb_kwargs = {
                "city_airline_date_code": city_airline_date_code,
            }
                
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_tickets_table,
                method=self.request_method,
                body=self.curl_request_raw_payload,
                cb_kwargs=cb_kwargs,
                meta=response.meta)
