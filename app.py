# -*- coding: utf-8 -*-

import json
import os
import time
from pathlib import Path
from typing import Dict, List

from alive_progress import alive_bar
from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions

from colors import bcolors
from filters import (passed_base_filters, passed_phase_filter,
                     passed_stickers_filter)
from market import get_new_items_from_market
from utils import get_search_items, load_cokies_to_driver

# Init browser
driver_path = Path(__file__).resolve().parent
driver_path = os.path.join(driver_path, 'chromedriver')

options = ChromeOptions()
options.add_argument('--headless')

driver = Chrome(options=options)
driver.get('https://lis-skins.ru/')
load_cokies_to_driver(driver, 'cookies_to_driver.json')

wait = WebDriverWait(driver, 10)


def purchase_skin(item_data: dict) -> None:
    driver.get(item_data['url'])
    driver.find_element(By.CSS_SELECTOR, f'.item.row.market_item.market_item_{item_data["site_id"]} .buy-now').click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'buy-now-popup-button.buy-now-popup-bottom-button'))).click()
    
    with open('cookies_to_driver.json', 'w', encoding='utf-8') as file_obj:
        file_obj.write(json.dumps({
                cookie.get('name'):cookie.get('value')
                for cookie in driver.get_cookies()
            }, indent=4, ensure_ascii=False),
        )

        
def get_items_to_purchase(new_items_id: List[Dict], search_items: List[Dict]) -> List[Dict]:
    items_to_purchase = []
    
    with alive_bar(len(new_items_id)) as bar:
        for shop_item_data in new_items_id:
            for search_item_data in search_items:
                if passed_base_filters(search_item_data, shop_item_data):
                    if passed_phase_filter(shop_item_data, search_item_data, driver) or \
                        passed_stickers_filter(shop_item_data, search_item_data):
                            items_to_purchase.append(shop_item_data)
                            continue
                    items_to_purchase.append(shop_item_data)
            bar()
    return items_to_purchase


def main() -> None:
    items_url_storage = []
    
    while True:
        search_items = get_search_items('search.json')

        new_items_data, items_url_storage = get_new_items_from_market(items_url_storage, driver)
        logger.debug(f'Geted new items {len(new_items_data)}')
         
        if len(new_items_data) > 0:
            logger.debug(
                f'Geted new skins from site {json.dumps(new_items_data, indent=2, ensure_ascii=False)} \n ' +\
                f'Total items {bcolors.OKBLUE}{len(new_items_data)}{bcolors.ENDC}',
            )
            items_to_purchase = get_items_to_purchase(new_items_data, search_items)
            logger.debug(f'Items to purchase {items_to_purchase}')
               
            for item_data in items_to_purchase:
                purchase_skin(item_data)
        time.sleep(5)

                
if __name__ == "__main__":
    try:
        main() 
    except KeyboardInterrupt:
        driver.quit()
        logger.warning('User stopped program')
