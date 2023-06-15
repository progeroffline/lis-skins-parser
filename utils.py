# -*- coding: utf-8 -*-

import json
from typing import Dict, List


def load_cokies_to_driver(driver: 'undetected_chromedriver.Chrome', filename: str,) -> None:
    with open(filename, 'r') as file_obj:
        cookies =  json.load(file_obj)
        for name, value in cookies.items():
            driver.add_cookie({'name': name, 'value': value})
            
     
def get_search_items(filename: str) -> List[Dict]:
    with open(filename, 'r'):
        return json.load(open('search.json')).get('items')
