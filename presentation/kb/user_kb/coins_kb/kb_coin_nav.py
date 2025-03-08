import math

from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import L
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from presentation.kb.user_kb.coins_kb.kb_coin_back import BackCoinsNavigation
from presentation.kb.user_kb.coins_kb.kb_coin_checktime import CoinCheckTime
from presentation.kb.user_kb.coins_kb.kb_coin_delete import DeleteCoin
from presentation.kb.user_kb.coins_kb.kb_coin_difference import CoinDifference


class CoinDetail(CallbackData, prefix="CoinDetail"):
    coinname: str


kb_coin_detail = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=L.COIN.DELETE(), callback_data=DeleteCoin().pack())],
        [
            InlineKeyboardButton(
                text=L.COIN.DIFFERENCE(), callback_data=CoinDifference().pack()
            )
        ],
        [
            InlineKeyboardButton(
                text=L.GENERAL.BACK(), callback_data=BackCoinsNavigation().pack()
            )
        ],
    ]
)


class CoinsNavigation(CallbackData, prefix="CoinNavigation"):
    page: int


def kb_coins_managment(coins, current_page: int = 1):
    inline_kb = []

    # if items less then pages exist before -> Leave to 1 page
    if len(coins) < (current_page * 10) - 9:
        current_page = 1

    total_pages = math.ceil(len(coins) / 10)
    start_index = (current_page - 1) * 10
    end_index = min(start_index + 10, len(coins))

    # load from db
    for i in range(start_index, end_index):
        inline_kb.append(
            [
                InlineKeyboardButton(
                    text=f"{coins[i]['coin_label']} {round(float(coins[i]['last_value']), 2)}$",
                    callback_data=CoinDetail(coinname=coins[i]["coinname"]).pack(),
                )
            ]
        )

    if len(coins) > 10:
        nav = []

        if current_page > 1:
            nav.append(
                InlineKeyboardButton(
                    text="◀️",
                    callback_data=CoinsNavigation(page=current_page - 1).pack(),
                )
            )

        nav.append(
            InlineKeyboardButton(
                text=f"{current_page}/{total_pages}", callback_data="None"
            )
        )

        if current_page < total_pages:
            nav.append(
                InlineKeyboardButton(
                    text="▶️",
                    callback_data=CoinsNavigation(page=current_page + 1).pack(),
                )
            )

        inline_kb.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=inline_kb)
