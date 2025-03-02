from aiogram.fsm.state import StatesGroup, State


class DeleteCoinState(StatesGroup):
    Confirmation = State()
