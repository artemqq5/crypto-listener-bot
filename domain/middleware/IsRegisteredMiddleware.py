from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject

from data.repositories.UserRepository import UserRepository


class IsUserRegisteredMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, (types.Message, types.CallbackQuery)):
            return

        user = event.from_user

        if not await UserRepository().user(user.id):
            await UserRepository().add_user(
                user.id, user.first_name, user.username, user.language_code
            )

        return await handler(event, data)
