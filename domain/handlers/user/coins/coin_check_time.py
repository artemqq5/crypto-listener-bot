from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from data.repositories.SettingValuesRepository import SettingValuesRepository
from domain.states.SetCheckTimeState import SetCheckTimeState
from domain.use_cases.UpdateTaskTracking import UpdateTaskTracking

router = Router()


@router.message(SetCheckTimeState.Time)
async def set_check_time(message: Message, i18n: I18nContext, state: FSMContext):
    try:
        checktime = int(message.text)
        if checktime > 180 or checktime < 1:
            raise ValueError
    except ValueError:
        await message.answer(i18n.COIN.CHECK_TIME.VALUE_ERROR())
        return

    if not await SettingValuesRepository().update_param("check_time", checktime):
        await message.answer(i18n.COIN.CHECK_TIME.FAIL())
        return

    await message.answer(i18n.COIN.CHECK_TIME.SUCCESS(check_time=checktime))
    await UpdateTaskTracking.reset_timers()
