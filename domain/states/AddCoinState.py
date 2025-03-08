from aiogram.fsm.state import State, StatesGroup


class AddCoinState(StatesGroup):
    GetCoin = State()
    Diference = State()
