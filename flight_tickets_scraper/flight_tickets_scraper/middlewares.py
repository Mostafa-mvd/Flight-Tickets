# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
import requests

from urllib.parse import urlencode
from random import randint

from scrapy import signals

from stem.control import Controller
from stem import Signal
from stem.util.log import get_logger


logger = get_logger()
logger.propagate = False


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class FlightTicketsScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class FlightTicketsScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapeOpsFakeUserAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        
        self.scrapeops_endpoint = settings.get(
            'SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 
            'http://headers.scrapeops.io/v1/user-agents?')
        
        self.scrapeops_fake_user_agents_active = settings.get(
            'SCRAPEOPS_FAKE_USER_AGENT_ENABLED', 
            False)
        
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')

        self.headers_list = []

        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()

    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint,
                                params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])

    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]

    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        self.scrapeops_fake_user_agents_active = True

    def process_request(self, request, spider):
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent


class TorMiddleware:
    def __init__(self, 
                 intermediate_proxy_url: str, 
                 ip_checker_site: str,
                 tor_changing_ip_delay_sec: int = 10,
                 tor_control_port: int = 9051, 
                 tor_randomize_changing_ip_delay: bool = False,
                 tor_password: str = None) -> None:
        
        self.intermediate_proxy_url = intermediate_proxy_url
        self.ip_checker_site = ip_checker_site
        self.tor_changing_ip_delay_sec = tor_changing_ip_delay_sec
        self.tor_control_port = tor_control_port
        self.tor_randomize_changing_ip_delay = tor_randomize_changing_ip_delay
        self.tor_password = tor_password

        self.last_time_ip_changed = 0
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        intermediate_proxy_url = settings.get('INTERMEDIATE_PROXY')
        ip_checker_site = settings.get("IP_CHECKER_SITE")
        tor_changing_ip_delay_sec = settings.get('TOR_CHANGING_IP_DELAY_SEC')
        tor_control_port = settings.get('TOR_CONTROL_PORT')
        tor_randomize_changing_ip_delay = settings.get('TOR_RANDOMIZE_CHANGING_IP_DELAY')
        tor_password = settings.get('TOR_PASSWORD')

        return cls(
            intermediate_proxy_url,
            ip_checker_site,
            tor_changing_ip_delay_sec,
            tor_control_port,
            tor_randomize_changing_ip_delay,
            tor_password)

    def _connect_to_tor(self, spider):
        controller = Controller.from_port(port=self.tor_control_port)

        if self.tor_password:
            controller.authenticate(password=self.tor_password)
            spider.logger.debug('Authentication has done correctly.')
        
        spider.logger.debug('Connection to tor through control port is established.')

        return controller
    
    def _change_ip_address(self, spider):
        with self._connect_to_tor(spider) as controller:
            controller.signal(Signal.NEWNYM)

            spider.logger.debug('Your tor ip changed.')

        spider.logger.debug('Tor connection is closed now.')

    def _set_new_ip(self, spider) -> None:
        self._change_ip_address(spider)

        current_tor_ip = self._exit_tor_node_ip_address()

        spider.logger.info(f'Tor exit node ip: {current_tor_ip}\n')

        self._set_tor_randomize_changing_ip_delay_or_fixed()

        self.last_time_ip_changed = time.time()
    
    def _exit_tor_node_ip_address(self):
        proxy = dict()
        protocol, domain_port = self.intermediate_proxy_url.split("://")
        proxy[protocol] = domain_port

        response = requests.get(
            url=self.ip_checker_site,
            proxies=proxy)
        
        return response.text.strip()
    
    def _set_tor_randomize_changing_ip_delay_or_fixed(self):
        if self.tor_randomize_changing_ip_delay:
            self.tor_randomize_changing_ip_delay = self._choose_random_number_between(
                0.5 * self.tor_randomize_changing_ip_delay,
                1.5 * self.tor_randomize_changing_ip_delay)

    def _choose_random_number_between(self, min_number, max_number):
        return round(random.uniform(min_number, max_number), 1)

    def process_request(self, request, spider) -> None:
        now = time.time()

        if now - self.last_time_ip_changed > self.tor_changing_ip_delay_sec:
            self._set_new_ip(spider)

        request.meta['proxy'] = self.intermediate_proxy_url
