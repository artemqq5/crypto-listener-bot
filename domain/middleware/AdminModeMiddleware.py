from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject

from config import ADMINS


class AdminModeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, (types.Message, types.CallbackQuery)):
            return

        user = event.from_user

        if user.id in ADMINS:
            return await handler(event, data)
