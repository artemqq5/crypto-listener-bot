import logging

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from data.BaseRepository import BaseRepository
from data.sqlmodels import User


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__()
        self.async_session = sessionmaker(self.engine, class_=AsyncSession)

    async def add_user(self, user_id: int, username: str, firstname: str, lang: str):
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = insert(User).values(user_id=user_id, username=username, firstname=firstname, lang=lang)
                    result = await session.execute(stmt)
                    return result.rowcount
        except Exception as e:
            logging.error(e)
            return None

    async def user(self, user_id) -> dict | None:
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = select(User).where(User.user_id == user_id)
                    result = await session.execute(stmt)
                    user = result.scalar_one_or_none()
                    return dict(user)
        except Exception as e:
            logging.error(e)
            return None
