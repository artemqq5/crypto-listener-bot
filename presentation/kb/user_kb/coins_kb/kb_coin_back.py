from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup


class BackCoinsNavigation(CallbackData, prefix="BackCoinsNavigation"):
    pass


class BackCoinNavigation(CallbackData, prefix="BackCoinNavigation"):
    pass


kb_back_coins_nav = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=L.GENERAL.BACK(), callback_data=BackCoinsNavigation().pack()
            )
        ]
    ]
)
