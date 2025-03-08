from aiogram.fsm.state import State, StatesGroup


class DeleteCoinState(StatesGroup):
    Confirmation = State()
