from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L
from aiogram_i18n.types import InlineKeyboardMarkup, InlineKeyboardButton

from presentation.kb.user_kb.coins_kb.kb_coin_back import BackCoinsNavigation


class DeleteCoin(CallbackData, prefix="DeleteCoin"):
    pass


class ConfirmationDeleteCoin(CallbackData, prefix="ConfirmationDeleteCoin"):
    pass


kb_confirmation_delete_coin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=L.GENERAL.CONFIRM(), callback_data=ConfirmationDeleteCoin().pack())],
    [InlineKeyboardButton(text=L.GENERAL.BACK(), callback_data=BackCoinsNavigation().pack())]
])
