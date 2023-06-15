# -*- coding: utf-8 -*-

import os

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': '*/*',
    'Accept-Language': 'ru',
    'Content-type': 'application/x-www-form-urlencoded',
    'Proxy-Authorization': 'Basic bS1tQGluYm94LnJ1Om16Zm54QnpGeDg1eHhnbTc4Tkdm',
    'Connection': 'keep-alive',
    'Referer': 'https://saveweb2zip.com/ru',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'If-None-Match': 'W/"2-nOO9QiTIwXgNtWtBJezz8kv3SLc"',
}

def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def get_page_source(url: str) -> BeautifulSoup:
    params = {
        'formOptions': '{"websiteLink":"{url}","isIntegration":false,"selectedIntegration":"email","intagrationData":{},"isLandUnique":false,"isAllPageDownload":false,"confirmLanguage":"RU","isMobileVersion":false,"isDefaultDownload":false}',
    }
    params['formOptions'] = params['formOptions'].replace('{url}', url)
    
    response = requests.get('https://saveweb2zip.com/api/landscrape', params=params, headers=headers)

    zip_file_url = None
    while zip_file_url is None:
        response = requests.get('https://saveweb2zip.com/api/checkProgress', params=params, headers=headers).json()
        zip_file_url = response.get('url')

    download_url(zip_file_url, 'url.zip')

    os.system('unzip -o -qq url.zip')
    os.system('rm -f url.zip index_1.html favicon.ico v1 ')
    os.system('rm -f images/ css/ -rd')

    response = None
    with open('index.html', 'r', encoding='utf-8') as file_obj:
        response = BeautifulSoup(file_obj.read(), 'html.parser')

    os.system('rm index.html')
    return response
