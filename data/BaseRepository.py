from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import create_async_engine

from config import DB_LINK_CONNECTION
from data.sqlmodels import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self):
        self.engine = create_async_engine(DB_LINK_CONNECTION)

    async def create_tables(self):
        """Створює всі таблиці, якщо вони не існують"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
