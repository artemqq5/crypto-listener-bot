from _decimal import Decimal

from unicodedata import decimal

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from data.repositories.CoinsRepository import CoinsRepository
from domain.states.AddCoinState import AddCoinState
from domain.use_cases.GetDataFromBinance import GetDataFromBinance

router = Router()


@router.message(AddCoinState.GetCoin)
async def name_or_url(message: Message, i18n: I18nContext, state: FSMContext):
    coin_html = GetDataFromBinance(message.text).get_binance_data()

    if not coin_html:
        await message.answer(i18n.COIN.NEW.FIND_FAIL())
        return

    await state.update_data(coin_html=coin_html)

    await message.answer(i18n.COIN.NEW.FIND_SUCCESS(
        coin_label=coin_html['coin_label'], price=coin_html['last_value'])
    )
    await state.set_state(AddCoinState.Diference)
    await message.answer(i18n.COIN.DIFFERENCE.SET(coin=coin_html['coin_label'], price=coin_html['last_value']))


@router.message(AddCoinState.Diference)
async def set_difference_value(message: Message, i18n: I18nContext, state: FSMContext):
    data = await state.get_data()
    coin_price = data['coin_html']['last_value']

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

    await message.answer(i18n.COIN.DIFFERENCE.SUCCESS(
        difference=difference, percent=percent, price=coin_price, coin=data['coin_html']['coin_label'])
    )

    data = await state.get_data()
    await state.clear()

    coin_html = data['coin_html']
    if not await CoinsRepository().add(
            coinname=coin_html['coinname'],
            coin_label=coin_html['coin_label'],
            last_value=coin_html['last_value'],
            difference_value=difference,
    ):
        await message.answer(i18n.COIN.NEW.FAIL(coin_label=coin_html['coin_label']))
        return

    await message.answer(i18n.COIN.NEW.SUCCESS(coin_label=coin_html['coin_label']))







