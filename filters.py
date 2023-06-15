# -*- coding: utf-8 -*-
from typing import Dict

import requests
import undetected_chromedriver

from steam import get_item_steam_url_wrap


def passed_base_filters(search_item_data: Dict, shop_item_data: Dict) -> bool:
    if shop_item_data.get('name') != search_item_data.get('name'): return False
    if shop_item_data.get('price_max') is not None:
        if shop_item_data['price_max'] > search_item_data.get('price'): return False
    
    if shop_item_data.get('float_min') is not None:
        if shop_item_data['float_min'] < search_item_data.get('float_value'): return False
    
    if shop_item_data.get('float_max') is not None:
        if shop_item_data['float_max'] > search_item_data.get('float_value'): return False
    
    return True


def passed_phase_filter(shop_item_data: Dict, search_item_data: Dict, driver: 'undetected_chromedriver.Chrome') -> bool:
    if search_item_data.get('phases') is not None:
        if search_item_data['phases'].get('seeds'):
            item_steam_url = get_item_steam_url_wrap(shop_item_data['site_id'], driver)
            response = requests.get(f'http://127.0.0.1:5000/?url={item_steam_url}').json()
            
            if response.get('iteminfo').get('paintseed') == search_item_data['phases']['seeds']:
                return True
    return False


def passed_stickers_filter(shop_item_data: Dict, search_item_data: Dict) -> bool:
    if 'stickers' in search_item_data:
        item_stickers = [ sticker_name for sticker_name in shop_item_data['stickers'] ]
        item_needed_stickers = [ i[0] for i in search_item_data['stickers'] ]
        
        for sticker in item_stickers:
            if sticker in item_needed_stickers: return True
    return False
