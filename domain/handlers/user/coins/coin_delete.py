from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from data.repositories.CoinsRepository import CoinsRepository
from domain.states.DeleteCoinState import DeleteCoinState
from presentation.kb.user_kb.coins_kb.kb_coin_back import kb_back_coins_nav
from presentation.kb.user_kb.coins_kb.kb_coin_delete import DeleteCoin, ConfirmationDeleteCoin, \
    kb_confirmation_delete_coin

router = Router()


@router.callback_query(DeleteCoin.filter())
async def coin_delete_call(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    data = await state.get_data()
    await state.set_state(DeleteCoinState.Confirmation)
    await callback.message.edit_text(i18n.COIN.DELETE.CONFIRM(coin=data['coin']['coin_label']),
                                     reply_markup=kb_confirmation_delete_coin)


@router.callback_query(ConfirmationDeleteCoin.filter(), DeleteCoinState.Confirmation)
async def coin_delete_confirm_call(callback: CallbackQuery, state: FSMContext, i18n: I18nContext):
    data = await state.get_data()

    if not await CoinsRepository().delete(data['coin']['coinname']):
        await callback.message.edit_text(i18n.COIN.DELETE.FAIL(coin=data['coin']['coin_label']),
                                         reply_markup=kb_back_coins_nav)
        return

    await callback.message.edit_text(i18n.COIN.DELETE.SUCCESS(coin=data['coin']['coin_label']),
                                     reply_markup=kb_back_coins_nav)
