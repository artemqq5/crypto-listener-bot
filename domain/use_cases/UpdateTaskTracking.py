import asyncio
import logging

from aiogram import Bot
from config import ADMINS

from data.repositories.CoinsRepository import CoinsRepository
from data.repositories.SettingValuesRepository import SettingValuesRepository
from domain.notification.notification_change_price import changed_price_coin
from domain.use_cases.GetDataFromBinance import GetDataFromBinance


class UpdateTaskTracking:
    """Клас для управління оновленням цін монет."""

    _tasks = {}  # Активні таски для монет
    _task_event = asyncio.Event()  # Подія для керування таймером
    _bot = None  # Екземпляр бота
    _i18n = None  # Контекст локалізації
    _last_notifications = {}  # Час останнього сповіщення для кожної монети
    _check_time = None  # Поточний час перевірки (оновлюється при зміні у БД)

    @classmethod
    def initialize(cls, bot: Bot, i18n):
        """Ініціалізує клас перед запуском, передаючи екземпляр бота та локалізацію."""
        cls._bot = bot
        cls._i18n = i18n

    @classmethod
    async def get_check_time_from_db(cls) -> int:
        """Отримує актуальний час перевірки з бази даних (у секундах) та оновлює глобальну змінну."""
        check_time = await SettingValuesRepository().param("check_time")
        if not check_time or "param_value" not in check_time:
            raise ValueError("⛔ Час перевірки відсутній у БД!")

        cls._check_time = (
            int(check_time["param_value"]) * 60
        )  # Переводимо хвилини в секунди
        return cls._check_time

    @classmethod
    async def update_check_time(cls):
        """Оновлює інтервал перевірки монет (якщо змінився у БД)."""
        try:
            new_check_time = await cls.get_check_time_from_db()
            if cls._check_time != new_check_time:
                logging.info(
                    f"🔄 Оновлення періоду перевірки: {cls._check_time // 60} → {new_check_time // 60} хв"
                )
                cls._check_time = new_check_time
                cls._task_event.set()  # Перезапускає всі таймери з новим періодом
        except ValueError as e:
            logging.error(e)

    @classmethod
    async def check_coin(cls, coin: dict):
        """Перевіряє ціну монети, але тепер НЕ викликає себе знову, а заново запускає весь цикл."""
        await cls.update_check_time()  # Перевіряємо чи змінився інтервал у БД

        logging.info(
            f"🔍 Починаємо перевірку {coin['coinname']} (інтервал: {cls._check_time // 60} хв)..."
        )

        await cls.check_coin_value(coin)

    @classmethod
    async def start_all_checks(cls):
        """Запускає перевірку для всіх монет. Завжди оновлює список перед запуском нового циклу."""
        try:
            await cls.get_check_time_from_db()  # Отримуємо початковий інтервал із БД
        except ValueError as e:
            logging.error(e)
            return

        coins = await CoinsRepository().coins()

        for coin in coins:
            coin_name = coin["coinname"]

            logging.info(
                f"🚀 Запускаємо перевірку для {coin_name} (кожні {cls._check_time // 60} хв)..."
            )
            await cls.check_coin(
                coin
            )  # Тепер запускаємо перевірку без створення зайвих тасків

        # Чекаємо або таймер, або команду `reset_timers()`
        try:
            await asyncio.wait_for(cls._task_event.wait(), timeout=cls._check_time)
        except asyncio.TimeoutError:
            pass  # Час вийшов, продовжуємо перевірку
        finally:
            cls._task_event.clear()  # Скидаємо подію після виконання

        # ❗ Після затримки заново викликаємо `start_all_checks()`, щоб отримати свіжі дані з БД
        asyncio.create_task(cls.start_all_checks())

    @classmethod
    async def reset_timers(cls):
        """Скидає таймери для всіх перевірок (виконує перевірку негайно)."""
        logging.info("⚡ Скидаємо всі таймери, перевірка запуститься негайно!")
        cls._task_event.set()  # Виконує всі перевірки негайно

    @classmethod
    async def check_coin_value(cls, coin_db: dict):
        """Перевіряє поточну ціну монети та відправляє сповіщення при зміні."""
        if cls._bot is None or cls._i18n is None:
            raise RuntimeError(
                "🚨 UpdateTaskTracking не ініціалізовано! Викличте UpdateTaskTracking.initialize(bot, i18n) перед стартом."
            )

        coin_html = GetDataFromBinance(coin_db["coinname"]).get_binance_data()
        if not coin_html:
            return

        new_price = coin_html["last_value"]
        old_price = coin_db["last_value"]
        difference = new_price - old_price

        current_time = asyncio.get_event_loop().time()
        last_notification_time = cls._last_notifications.get(coin_db["coinname"], 0)
        time_since_last_notification = current_time - last_notification_time

        logging.info(
            f"📊 {coin_db['coinname']} -> Стара ціна: {old_price}, Нова ціна: {new_price}, Різниця: {difference}"
        )

        if abs(difference) > coin_db["difference_value"]:
            if time_since_last_notification >= cls._check_time:
                logging.info(
                    f"📢 Сповіщення для {coin_db['coinname']} буде відправлено!"
                )

                await CoinsRepository().update_price(coin_db["coinname"], new_price)

                cls._last_notifications[coin_db["coinname"]] = current_time

                await changed_price_coin(
                    coin_label=coin_db["coin_label"],
                    difference=difference,
                    new_price=new_price,
                    old_price=old_price,
                    check_time=cls._check_time / 60,
                    user_id=ADMINS[0],
                    bot=cls._bot,
                    i18n=cls._i18n,
                )
            else:
                logging.info(
                    f"⏳ Пропускаємо сповіщення для {coin_db['coinname']} – ще не минув інтервал часу."
                )
