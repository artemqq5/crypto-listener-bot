from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from data.repositories.CoinsRepository import CoinsRepository
from domain.states.ChangeDifferenceCoinState import ChangeDifferenceCoinState
from domain.use_cases.GetDataFromBrowser import GetDataFromBrowser
from domain.use_cases.UpdateTaskTracking import UpdateTaskTracking
from presentation.kb.user_kb.coins_kb.kb_coin_back import kb_back_coins_nav
from presentation.kb.user_kb.coins_kb.kb_coin_difference import CoinDifference

router = Router()


@router.callback_query(CoinDifference.filter())
async def coin_change_difference_value_call(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    data = await state.get_data()
    coin_price = GetDataFromBrowser(data['coin']['coinname']).get_binance_data()['last_value']
    await state.update_data(coin_price=coin_price)
    await callback.message.edit_text(i18n.COIN.DIFFERENCE.SET(
        coin=data['coin']['coin_label'], price=coin_price),
        reply_markup=kb_back_coins_nav
    )
    await state.set_state(ChangeDifferenceCoinState.Difference)


@router.message(ChangeDifferenceCoinState.Difference)
async def set_difference_value(message: Message, i18n: I18nContext, state: FSMContext):
    data = await state.get_data()
    coin_price = data['coin_price']

    if "%" in message.text:
        try:
            difference = int(message.text.rstrip("%"))  # Видаляємо % і конвертуємо у число
            if not (1 <= difference <= 100):  # Перевірка діапазону
                raise ValueError

            difference = round((coin_price / 100) * difference, 2)
            percent = difference / coin_price * 100  # Відсоткове співвідношення
        except ValueError:
            await message.answer(i18n.COIN.DIFFERENCE.VALUE_ERROR())
            return
    else:
        try:
            difference = round(float(message.text), 2)  # Конвертуємо у float і округлюємо
            if not (0.01 <= difference <= 1000):  # Перевірка діапазону
                raise ValueError

            percent = round((difference / coin_price) * 100, 2)  # Відсоткове співвідношення
        except ValueError:
            await message.answer(i18n.COIN.DIFFERENCE.VALUE_ERROR())
            return

    if not await CoinsRepository().update_difference(data['coin']['coinname'], difference):
        await message.answer(i18n.COIN.DIFFERENCE.FAIL(
            coin=data['coin']['coin_label']),
            reply_markup=kb_back_coins_nav
        )
        return

    await message.answer(i18n.COIN.DIFFERENCE.SUCCESS(
        difference=difference, percent=percent, price=coin_price, coin=data['coin']['coin_label']),
        reply_markup=kb_back_coins_nav
    )

    await UpdateTaskTracking.reset_timers()