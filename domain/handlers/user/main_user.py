from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from data.repositories.CoinsRepository import CoinsRepository
from data.repositories.SettingValuesRepository import SettingValuesRepository
from domain.handlers.user.coins import coin_nav
from domain.states.AddCoinState import AddCoinState
from domain.states.SetCheckTimeState import SetCheckTimeState
from presentation.kb.user_kb.coins_kb.kb_coin_nav import kb_coins_managment

router = Router()

router.include_routers(
    coin_nav.router,
)


@router.message(Command("start"))
async def start(message: Message, i18n: I18nContext, state: FSMContext):
    check_time = await SettingValuesRepository().param('check_time')
    await message.answer(i18n.GENERAL.START_MESSAGE(check_time=check_time['param_value']))


@router.message(Command("new"))
async def new_coin(message: Message, i18n: I18nContext, state: FSMContext):
    await message.answer(i18n.COIN.NEW.GET())
    await state.set_state(AddCoinState.GetCoin)


@router.message(Command("coins"))
async def coins(message: Message, i18n: I18nContext, state: FSMContext):
    coin_list = await CoinsRepository().coins()
    await message.answer(i18n.COIN.MY_COINS(), reply_markup=kb_coins_managment(coin_list))


@router.message(Command("checktime"))
async def checktime(message: Message, i18n: I18nContext, state: FSMContext):
    await message.answer(i18n.COIN.CHECK_TIME.SET())
    await state.set_state(SetCheckTimeState.Time)
