# Proxy Rotation With Tor

import requests
import re

from stem import Signal
from stem.process import launch_tor_with_config
from stem.control import Controller

from toripchanger import TorIpChanger


def send_requests(url, proxies=None):
    return requests.get(
        url=url, 
        proxies=proxies)


def set_new_tor_ip1():
    SOCKS_PORT = '9050'
    CONTROL_PORT = '9051'

    tor_process = launch_tor_with_config(
        config={
            'SocksPort': SOCKS_PORT,
            'ControlPort':  CONTROL_PORT,
            'MaxCircuitDirtiness': '20',
        },
        init_msg_handler=lambda line: print(line) if re.search(
            'Bootstrapped', line) else False,
    )

    return tor_process

def set_new_tor_ip2():
    tor_ip_changer = TorIpChanger(
        reuse_threshold=0,
        tor_password='SigmaZ2015',
        tor_port=9051,
        local_http_proxy='127.0.0.1:8118')

    tor_ip_changer.get_new_ip()


def set_new_tor_ip3():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="SigmaZ2015")
        controller.signal(Signal.NEWNYM)


# The response from these sites should show the IP address of the Tor exit node, instead of your own ---

urls = [
        'http://icanhazip.com/',
        'http://ip-api.com/json/',
        'https://api.myip.com/',
    ]

# Prixoxy for connecting your request to tor network
PROXIES = {
        'http': '127.0.0.1:8118',
        'https': '127.0.0.1:8118',
    }


response = requests.get(urls[0])
current_ip = response.text.strip()

for url in urls:
    tor_p = set_new_tor_ip1()
    response = send_requests(url, PROXIES)
    tor_p.kill()
