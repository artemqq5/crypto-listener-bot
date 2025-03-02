import logging

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class GetDataFromBrowser:
    def __init__(self, url_or_coin):
        self.url = self.normalize_url(url_or_coin)
        self.coin_name = self.extract_coin_name(self.url)
        self.soup = None

    def normalize_url(self, input_data):
        """Перевіряє, чи є введені дані посиланням, і приводить його до правильного формату."""
        if input_data.startswith("https"):
            return input_data
        return f"https://www.binance.com/en/price/{input_data.lower()}"

    def extract_coin_name(self, url):
        """Витягує назву монети з URL."""
        parsed_url = urlparse(url)
        return parsed_url.path.split("/")[-1].lower()

    def fetch_page(self):
        """Завантажує HTML-сторінку."""
        response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Помилка при завантаженні сторінки: {response.status_code}")

    def get_binance_data(self):
        """Отримує дані про монету з Binance."""
        try:
            self.url = f"https://www.binance.com/en/price/{self.coin_name}"
            self.fetch_page()

            coin_label = self.soup.select_one("h1.my-0.flex-grow.text-textPrimary")
            if coin_label:
                coin_label = coin_label.text.replace(" Price", "").strip()
            else:
                return None

            price = self.soup.select_one("span.t-subtitle2.text-textPrimary")
            if price:
                price = round(float(price.text.split(" ")[3].replace("$", "")), 2)
            else:
                return None
            return {"coinname": self.coin_name, "coin_label": coin_label, "last_value": price}
        except Exception as e:
            logging.info(e)
            return None

