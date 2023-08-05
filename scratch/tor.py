# Proxy Rotation With Tor


import json
import requests
import re


from bs4 import BeautifulSoup

from stem import Signal
from stem.process import launch_tor_with_config, launch_tor
from stem.control import Controller

from toripchanger import TorIpChanger

from time import sleep, time


def send_requests(url, proxies=None):
    return requests.get(
        url=url, 
        proxies=proxies)


def set_new_tor_ip1():
    SOCKS_PORT = '9050'
    CONTROL_PORT = '9051'
    MAX_CIRCUIT_DIRTINESS = '20'

    # This writes a temporary torrc to disk.
    tor_process = launch_tor_with_config(
        config={
            'SocksPort': SOCKS_PORT,
            'ControlPort': CONTROL_PORT,
            'MaxCircuitDirtiness': MAX_CIRCUIT_DIRTINESS,
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


def connect_to_tor(password=None):
    # # This writes a temporary torrc to disk.
    # Controller used to talk with Tor and the circuit will be built by it.
    # The ControlPort is the port to control the Tor instance.

    controller = Controller.from_port(port=9051)

    if password:
        controller.authenticate(password)

    return controller

def change_ip_address(pwd=None):
    global last_time_ip_changed

    with connect_to_tor(pwd) as controller:
        controller.signal(Signal.NEWNYM)

    last_time_ip_changed = time()


def set_new_tor_ip3(tor_download_delay=1, pwd=None):
    global last_time_ip_changed
    if time() - last_time_ip_changed > tor_download_delay:
        change_ip_address(pwd)


# The response from these sites should show the IP address of the Tor exit node, instead of your own ---

urls = [
        'https://check.torproject.org/',
        'http://icanhazip.com/',
        'http://ip-api.com/json/',
        'https://api.myip.com/',
    ]

# Privoxy for connecting your request to tor network
PROXIES = {
        'http': '127.0.0.1:8118',
        'https': '127.0.0.1:8118',
    }


response = requests.get(urls[1])
current_ip = response.text.strip()
interval = 15
password = "SigmaZ2015"
last_time_ip_changed = interval

for idx, url in enumerate(urls):
    set_new_tor_ip3(interval, password)
    
    response = send_requests(url, PROXIES)

    if idx == 0:
        soup = BeautifulSoup(response.text, 'html.parser')
        tor_exit_node_ip = soup.find('strong').text
        sleep(interval + 1)
    elif idx == 1:
        tor_exit_node_ip = response.text.strip()
    elif idx == 2:
        tor_exit_node_ip = json.loads(response.content)['query']
        sleep(interval + 1)
    elif idx == 3:
        tor_exit_node_ip = json.loads(response.content)['ip']
    
    print(tor_exit_node_ip)
    
    #tor_p.kill()
