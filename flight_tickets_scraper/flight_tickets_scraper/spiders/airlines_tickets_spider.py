from scrapy_selenium import SeleniumRequest

from selenium.webdriver.common.by import By

import scrapy


class AirlinesTickets(scrapy.Spider):
    name = "airlines_tickets"

    def start_requests(self):
        url = "https://www.tcharter.ir/"
        yield SeleniumRequest(
            url=url, 
            callback=self.parse,
            wait_time=2)

    def parse(self, response, **kwargs):
        driver = response.request.meta['driver']
        #elm = response.css("#result-THR+ .green-medium .text-start")
        button = driver.find_elements(
            By.CSS_SELECTOR, 
            "#result-THR+ .green-medium .text-start")
        button.click()
