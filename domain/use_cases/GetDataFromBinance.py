import logging
from urllib.parse import urlparse

import requests


class GetDataFromBinance:
    BASE_URL = "https://api.binance.com/api/v3/ticker/price"

    def __init__(self, input_data):
        """Приймає символ монети (у будь-якому регістрі)."""
        self.coinname = self.extract_coin_name(input_data)
        self.symbol = (
            f"{self.coinname.upper()}USDT"  # Binance використовує пари, напр. BTCUSDT
        )

    def extract_coin_name(self, input_data):
        coin_name = input_data  # Якщо не URL, просто використовуємо введене значення
        return (
            coin_name.upper().strip()
        )  # Робимо символ великими літерами і прибираємо пробіли

    def get_binance_data(self):
        """Отримує ціну монети з Binance API."""
        url = f"{self.BASE_URL}?symbol={self.symbol}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Викине помилку, якщо статус-код не 200

            data = response.json()

            # Перевіряємо, чи є ключ "price" у відповіді
            if "price" not in data:
                logging.error(
                    f"⚠️ Binance API не повернув 'price' для {self.symbol}: {data}"
                )
                return None

            # Перетворюємо рядок у float і округлюємо до 2 знаків
            price = round(float(data["price"]), 5)

            return {
                "coinname": self.coinname,
                "coin_label": self.coinname,  # Binance API не повертає красиве ім'я
                "last_value": price,
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Помилка запиту до Binance API: {e}")
            return None
