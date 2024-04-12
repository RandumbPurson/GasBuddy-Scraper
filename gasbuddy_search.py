from bs4 import BeautifulSoup
from typing import Literal

from getHTML import getHTML

fuelTypeMap = {"regular": 1, "midgrade": 2, "premium":3}
price_class = "text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL"
address_class = "StationDisplay-module__address___2_c7v"
header_class = "header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8"

def get_brands(soup):
    return [el.find("a").get_text() for el in soup.find_all(class_=header_class)]

def get_addresses(soup): 
    return [el.get_text() for el in soup.find_all(class_=address_class)]

def process_price(price):
    if "$" in price:
        return float(price.replace("$", ""))
    else:
        return None
def get_prices(soup): 
    return [process_price(el.get_text()) for el in soup.find_all(class_=price_class)]

class Search:
    def __init__(self, **kwargs):
        self.payload = {}
        self.ua = UserAgent(**kwargs)

    def search(self, val):
        """ search for a city, place, or zip code
        """
        self.payload["search"] = val
        return self
    
    def fuelType(self, val: Literal["regular", "midgrade", "premium"]):
        """ search prices for a fuel type
        One of: regular, midgrade, premium
        """
        self.payload["fuel"] = fuelTypeMap[val]
        return self

    def payMethod(self, val: Literal["all", "credit"]):
        """ filter by payment method
        One of: all, credit
        """
        self.payload["method"] = val
        return self

    def lastUpdated(self, val: Literal[4, 8]):
        """ filter by time since last updated
        One of: 4, 8
        """
        self.payload["maxAge"] = val
        return self

    def get(self, max_expands=100):
        """ get the data
        """
        html = getHTML("https://www.gasbuddy.com/home", self.payload, max_expands)
        soup = BeautifulSoup(html, features="html.parser")
        data = {
            "addresses": get_addresses(soup),
            "brands": get_brands(soup),
            "prices": get_prices(soup)
        }
        return data
