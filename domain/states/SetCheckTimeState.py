from aiogram.fsm.state import State, StatesGroup


class SetCheckTimeState(StatesGroup):
    Time = State()
