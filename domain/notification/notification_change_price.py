import logging

from aiogram import Bot
from aiogram_i18n import I18nContext

from data.repositories.UserRepository import UserRepository


async def changed_price_coin(coin_label, difference, new_price, old_price, check_time, user_id: int, bot: Bot,
                             i18n: I18nContext):
    user = await UserRepository().user(user_id)

    try:
        with i18n.use_locale(user.get('lang', 'en')):
            await bot.send_message(
                chat_id=user['user_id'],
                text=i18n.NOTIFY.COIN_CHANGED_PRICE(
                    coin_label=coin_label,
                    difference=difference,
                    new_price=new_price,
                    old_price=old_price,
                    check_time=check_time
                )
            )
    except Exception as e:
        logging.error(f"Messaging: Failed to notify changed_price_coin: {e}")
