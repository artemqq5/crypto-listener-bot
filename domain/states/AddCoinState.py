from aiogram.fsm.state import StatesGroup, State


class AddCoinState(StatesGroup):
    GetCoin = State()
    Diference = State()
