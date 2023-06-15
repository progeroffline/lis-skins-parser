# -*- coding: utf-8 -*-
import json
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from skin_html_page_parser import SkinHtmlPageParser


def get_item_json_data(items_url: List[str], driver: 'undetected_chromedriver.Chrome') -> List[Dict]:
    items_json_data = []
    for url in items_url:
        driver.get(url)
        item_parser = SkinHtmlPageParser(driver.page_source)        
        try: 
            items_json_data.append({
                'name': item_parser.name,
                'site_id': item_parser.site_id,
                'float_value': item_parser.float_value,
                'stickers': item_parser.stickers,
                'price': item_parser.price,
                'url': url,
            })
        except:
            print(url, item_parser.float_value, item_parser.name, item_parser.site_id)
    return items_json_data


def get_new_items_from_market(items_id_storage, driver: 'undetected_chromedriver.Chrome') -> Tuple[List[Dict], List[int]]:
    params = {
        'sort_by' : 'date_desc',
        'exterior' : '2,4,3,6,1,5',
        'ajax': '1',
    } 
    url = 'https://lis-skins.ru/market/csgo/?' 
    url += ''.join([
        f'{key}={value}&'
        for key, value in params.items()
        if value is not None
    ])
    
    driver.get(url)
    content = driver.find_element(By.TAG_NAME, 'pre').text
    parsed_json = json.loads(content)
    
    items = BeautifulSoup(parsed_json.get('skins'), 'html.parser')
    items_url = [
        item['data-link'] 
        for item in items.find_all('div', attrs={'class': 'market_item'})
    ]
    
    if len(items_id_storage) == 0:
        return [], items_url
    
    items_url = list(set([ item_url for item_url in items_url if item_url not in items_id_storage ]))
    items_id_storage += items_url
    items_json_data = get_item_json_data(items_url, driver)

    return items_json_data, items_id_storage
