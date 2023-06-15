# -*- coding: utf-8 -*-

import random
import time

import requests

from colors import bcolors

params = {
    'l': 'russian',
    'count': '75',
}

proxies = [
    '38640:8h6IHkCp@195.123.178.220:2831',
    '38641:PYgslF9u@193.22.97.185:2831',
    '38639:3DHnf32E@185.174.102.60:2831',
    'icelifenitro55:8gZzitIb@185.112.12.34:2831',
    'icelifenitro55:8gZzitIb@185.112.13.30:2831',
    'icelifenitro55:8gZzitIb@185.112.14.2:2831',
    'icelifenitro55:8gZzitIb@185.112.15.16:2831',
    'icelifenitro55:8gZzitIb@212.86.111.235:2831',
    '38663:OIg06KOx@51.68.185.139:2831',
    '38663:OIg06KOx@51.77.70.233:2831',
    '38663:OIg06KOx@51.89.14.144:2831',
    '38663:OIg06KOx@51.89.89.98:2831',
    '38663:OIg06KOx@51.195.72.153:2831',
    '38663:OIg06KOx@51.195.124.203:2831',
    '38663:OIg06KOx@135.125.166.195:2831',
    '38663:OIg06KOx@135.125.166.254:2831',
    '38663:OIg06KOx@135.125.173.86:2831',
    '38663:OIg06KOx@135.125.192.96:2831',
    '38663:OIg06KOx@135.125.210.184:2831',
    '38663:OIg06KOx@135.125.215.220:2831',
    '38663:OIg06KOx@135.125.224.132:2831',
]
random.shuffle(proxies)
proxies = { proxy:0 for proxy in proxies }

def up_proxy_usage(proxy: str, count: int):
    proxies[proxy] += count
   

def get_random_proxy() -> dict:
    proxy = min(proxies.items(), key=lambda x: x[1])
    proxy = proxy[0]
    proxies[proxy] += 1
    
    proxy = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    return proxy


def make_request_with_proxy(url: str):
    proxy = get_random_proxy() 
    response = requests.get(
        url=url,
        proxies=proxy,
    )

    if response.status_code == 200:
        print(bcolors.OKGREEN, response.status_code, bcolors.ENDC, proxy, url)
    else:
        print(bcolors.FAIL, response.status_code, bcolors.ENDC, proxy, url)
        up_proxy_usage(proxy['http'].replace('http://', ''), 5)
        time.sleep(5)

    return response.json()
