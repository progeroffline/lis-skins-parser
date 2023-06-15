# -*- coding: utf-8 -*-

from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag


class SkinHtmlPageParser():
    def __init__(self, html_document: str):
        """
        Initializes the SkinHtmlPageParser object.

        Parameters:
        - html_document (str): The HTML document for parsing.
        """
        self.html_document = BeautifulSoup(html_document, 'html.parser')
        self.name = self.get_name()
        self.site_id = self.get_site_id()
        self.float_value = self.get_float_value()
        self.stickers = self.get_stickers()
        self.price = self.get_price()
        
    def get_name(self) -> str:
        """
        Returns the name of the skin.

        Returns:
        - str: The name of the skin or 'None' if the name is not found.
        """
        name = self.html_document.find('div', attrs={'class': 'skin-name'})
        return name.text if name is not None else 'None'

    def get_site_id(self) -> str:
        """
        Returns the site ID of the skin.

        Returns:
        - str: The site ID of the skin or an empty string if the ID is not found.
        """
        site_id = self.html_document.find('a', attrs={'class': 'market-view-in-game-link'})
        site_id = site_id.get('data-id') if isinstance(site_id, Tag) else site_id
        return str(site_id)

    def get_float_value(self) -> float:
        """
        Returns the float value of the skin.

        Returns:
        - float: The float value of the skin or 0.0 if the value is not found.
        """
        float_value = ''.join([
            element.find('div', attrs={'class': 'spec-value'}).text
            for element in self.html_document.find_all('div', attrs={'class': 'spec-item'})
            if element.find('div', attrs={'class': 'spec-title'}).text == 'Float'
        ])
        return float(float_value)

    def get_stickers(self) -> List[str]:
        """
        Returns the list of stickers on the skin.

        Returns:
        - List[str]: The list of stickers on the skin or an empty list if no stickers are found.
        """
        stickers_list_block = self.html_document.find('div', attrs={'class': 'sticker-list'})
        if not isinstance(stickers_list_block, Tag):
            stickers = []
        else: 
            stickers = [
                element['title'] 
                for element in stickers_list_block.find_all('div', attrs={'class': 'sticker'})
            ]
        return stickers     

    def get_price(self) -> float:
        """
        Returns the price of the skin.

        Returns:
        - float: The price of the skin or 0.0 if the price is not found.
        """
        price = self.html_document.find('div', attrs={'class': 'min-price-value'})
        price = price.text.replace('$', '') if price is not None else 0.0
        return float(price) if not isinstance(price, float) else price
