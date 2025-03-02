from aiogram.types import User
from aiogram_i18n.managers import BaseManager

from data.repositories.UserRepository import UserRepository


class LocaleManager(BaseManager):

    async def set_locale(self, locale: str) -> str:
        pass

    async def get_locale(self, event_from_user: User) -> str:
        user = await UserRepository().user(event_from_user.id)
        return user["lang"] if user else event_from_user.language_code
