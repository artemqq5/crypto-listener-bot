import os

from dotenv import load_dotenv

load_dotenv()  # Зчитує .env файл

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_PATH = f"/crypto-listener-bot/{BOT_TOKEN}"
DB_LINK_CONNECTION = os.getenv("DB_LINK_CONNECTION")

admins_raw = os.getenv("ADMINS", "")
ADMINS = [int(x) for x in admins_raw.split(",") if x.strip()]
