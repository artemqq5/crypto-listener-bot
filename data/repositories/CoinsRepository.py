import logging

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from data.BaseRepository import BaseRepository
from data.sqlmodels import Coin


class CoinsRepository(BaseRepository[Coin]):
    def __init__(self):
        super().__init__()
        self.async_session = sessionmaker(self.engine, class_=AsyncSession)

    async def add(self, coinname, coin_label, last_value, difference_value):
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = insert(Coin).values(
                        coinname=coinname,
                        coin_label=coin_label,
                        last_value=last_value,
                        difference_value=difference_value,
                    )
                    result = await session.execute(stmt)
                    return result.rowcount
        except Exception as e:
            logging.error(e)
            return None

    async def delete(self, coinname):
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = delete(Coin).where(Coin.coinname == coinname)
                    result = await session.execute(stmt)
                    return result.rowcount
        except Exception as e:
            logging.error(e)
            return None

    async def update_difference(self, coinname, difference):
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = update(Coin).values(difference_value=difference).where(Coin.coinname == coinname)
                    result = await session.execute(stmt)
                    return result.rowcount
        except Exception as e:
            logging.error(e)
            return None

    async def update_price(self, coinname, price):
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = update(Coin).values(last_value=price).where(Coin.coinname == coinname)
                    result = await session.execute(stmt)
                    return result.rowcount
        except Exception as e:
            logging.error(e)
            return None

    async def coin(self, coinname):
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = select(Coin).where(Coin.coinname == coinname)
                    result = await session.execute(stmt)
                    coin = result.scalar_one_or_none()
                    return dict(coin) if coin else None
        except Exception as e:
            logging.error(e)
            return None

    async def coins(self):
        try:
            async with self.async_session() as session:
                async with session.begin():
                    stmt = select(Coin)
                    result = await session.execute(stmt)
                    coins = result.scalars().all()
                    return [dict(coin) for coin in coins]
        except Exception as e:
            logging.error(e)
            return None
