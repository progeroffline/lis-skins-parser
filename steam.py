# -*- coding: utf-8 -*-

import time
from typing import Union

from logzero import logger

from colors import bcolors
from download_site import get_page_source
from proxy_requests import make_request_with_proxy


def generate_item_url(inventory_id, asset_id) -> Union[str, None]:
    url = f'https://steamcommunity.com/inventory/{inventory_id}/730/2'
    response = make_request_with_proxy(url) 
    if response == None:
        time.sleep(1)
        return     
    
    class_id = None
    url = None
    for item in response.get('assets'):
        if item.get('assetid') == asset_id:
            class_id = item.get('classid') 
            break

    for item in response.get('descriptions'):
        if item.get('classid') == class_id:
            url = item.get('actions')[0].get('link')
            break
    
    if url is not None:
        url = url.replace('%owner_steamid%', inventory_id)
        url = url.replace('%assetid%', asset_id)
        return url  


def get_item_steam_url(item_id: str, driver: 'undetected_chromedriver.Chrome') -> Union[str, None]:
    url = f'https://lis-skins.ru/market/redirect/to-bot/{item_id}/'
    driver.get(url)
    
    item_url = driver.current_url
    asset_id = item_url.split('_')[-1]
    
    content = str(get_page_source(item_url))  
    
    search_word = 'UserYou.SetSteamId' 
    first_part_index = content.find(search_word)
    endline = content[first_part_index:].find(';')-3
    inventory_id = content[first_part_index+len(search_word)+3:first_part_index+endline]
    
    return generate_item_url(inventory_id, asset_id)



def get_item_steam_url_wrap(item_id: str, driver: 'undetected_chromedriver.Chrome') -> str:
    item_steam_url = None
    while item_steam_url is None:
        logger.debug(
            'Get url for https://lis-skins.ru/market/redirect/to-bot/{}/'.format(
                f'{bcolors.OKGREEN}{item_id}{bcolors.ENDC}'
            )
        )
        item_steam_url = get_item_steam_url(item_id, driver)
    return item_steam_url 
