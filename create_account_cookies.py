# -*- coding: utf-8 -*-

import json
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_auth_code() -> list:
    print('Get auth code...')
    json_data = json.load(open('auth_code.json', 'r', encoding='utf-8')) 
    print(f'Geted value {json_data}')
    
    if json_data.get('auth_code') is None or json_data.get('auth_code') == '':
        print('Auth code not found wait...')
        time.sleep(5)
        return get_auth_code()
    
    return list(json_data.get('auth_code'))


login_arg, password_arg = sys.argv[1:]

# Init browser
driver_path = Path(__file__).resolve().parent
driver_path = os.path.join(driver_path, 'chromedriver')

options = webdriver.ChromeOptions()
service = ChromeService(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

driver.get('https://lis-skins.ru/')
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'loginButton'))).click()
wait.until(EC.number_of_windows_to_be(2))
driver.switch_to.window(driver.window_handles[1])

login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"].newlogindialog_TextInput_2eKVn')))
password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"].newlogindialog_TextInput_2eKVn')))

login.send_keys(login_arg)
password.send_keys(password_arg)

driver.find_element(By.CSS_SELECTOR, '.newlogindialog_SubmitButton_2QgFE').click()

wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="text"].Focusable')))
input_chars = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"].Focusable')

auth_code = get_auth_code()
[ input.send_keys(char) for input, char in zip(input_chars, auth_code) ]
time.sleep(300)
