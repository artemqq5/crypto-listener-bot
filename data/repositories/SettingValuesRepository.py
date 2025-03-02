import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from data.BaseRepository import BaseRepository
from data.sqlmodels import SettingValue


class SettingValuesRepository(BaseRepository[SettingValue]):
    def __init__(self):
        super().__init__()
        self.async_session = sessionmaker(self.engine, class_=AsyncSession)

    async def param(self, param) -> dict | None:
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = select(SettingValue).where(SettingValue.param == param)
                    result = await session.execute(stmt)
                    param = result.scalar_one_or_none()
                    return dict(param)
        except Exception as e:
            logging.error(e)
            return None

    async def update_param(self, param, param_value) -> dict | None:
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = update(SettingValue).values(param_value=param_value).where(SettingValue.param == param)
                    result = await session.execute(stmt)
                    return result.rowcount
        except Exception as e:
            logging.error(e)
            return None
