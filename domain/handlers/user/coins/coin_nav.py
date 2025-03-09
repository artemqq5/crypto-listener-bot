from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from data.repositories.CoinsRepository import CoinsRepository
from domain.handlers.user.coins import (coin_add, coin_check_time, coin_delete,
                                        coin_difference_value)
from presentation.kb.user_kb.coins_kb.kb_coin_back import (BackCoinNavigation,
                                                           BackCoinsNavigation)
from presentation.kb.user_kb.coins_kb.kb_coin_nav import (CoinDetail,
                                                          CoinsNavigation,
                                                          kb_coin_detail,
                                                          kb_coins_managment)

router = Router()

router.include_routers(
    coin_add.router,
    coin_difference_value.router,
    coin_check_time.router,
    coin_delete.router,
)


@router.callback_query(CoinsNavigation.filter())
async def coins_nav_call(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    page = int(callback.data.split(":")[1])

    await state.update_data(last_page_coins=page)
    coin_list = await CoinsRepository().coins()

    await callback.message.edit_text(
        text=i18n.COIN.MY_COINS(),
        reply_markup=kb_coins_managment(coin_list, current_page=page),
    )


@router.callback_query(CoinDetail.filter())
async def coin_detail_call(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    coinname = callback.data.split(":")[1]
    coin = await CoinsRepository().coin(coinname)

    await state.update_data(coin=coin)

    await callback.message.edit_text(
        i18n.COIN.DETAIL(
            coin_label=coin["coin_label"],
            id=coin["id"],
            coinname=coin["coinname"],
            last_value=coin["last_value"],
            difference=coin["difference_value"],
        ),
        reply_markup=kb_coin_detail,
    )


@router.callback_query(BackCoinsNavigation.filter())
async def coins_back_call(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    data = await state.get_data()
    coin_list = await CoinsRepository().coins()

    await callback.message.edit_text(
        text=i18n.COIN.MY_COINS(),
        reply_markup=kb_coins_managment(
            coin_list, current_page=data.get("last_page_coins", 1)
        ),
    )


@router.callback_query(BackCoinNavigation.filter())
async def coin_back_call(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    data = await state.get_data()
    coin = await CoinsRepository().coin(data.get("coin", {}).get("coinname"))

    if not coin:
        await callback.answer(i18n.COIN.NOT_EXIST())
        return

    await state.update_data(coin=coin)

    await callback.message.edit_text(
        i18n.COIN.DETAIL(
            coin_label=coin["coin_label"],
            id=coin["id"],
            coinname=coin["coinname"],
            last_value=round(float(coin["last_value"]), 5),
            difference=coin["difference_value"],
        ),
        reply_markup=kb_coin_detail,
    )
