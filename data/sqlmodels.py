from sqlalchemy import (BigInteger, DateTime, Numeric, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=True)
    lang: Mapped[str] = mapped_column(String(2), nullable=True)
    joined: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())  # pylint: disable=not-callable

    __table_args__ = (UniqueConstraint("user_id", name="uq_user"),)

    def __iter__(self):
        yield from {
            "user_id": self.user_id,
            "username": self.username,
            "firstname": self.firstname,
            "lang": self.lang,
            "joined": self.joined.isoformat() if self.joined else None,
        }.items()


class Coin(Base):
    __tablename__ = "coins"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    coinname: Mapped[str] = mapped_column(String(255), nullable=False)
    coin_label: Mapped[str] = mapped_column(String(255), nullable=True)
    last_value: Mapped[float] = mapped_column(Numeric(6, 2), nullable=True)
    difference_value: Mapped[float] = mapped_column(
        Numeric(6, 2), nullable=False, default=10
    )

    __table_args__ = (UniqueConstraint("coinname", name="uq_coin"),)

    def __iter__(self):
        yield from {
            "id": self.id,
            "coinname": self.coinname,
            "coin_label": self.coin_label,
            "last_value": float(self.last_value) if self.last_value else None,
            "difference_value": float(self.difference_value),
        }.items()


class SettingValue(Base):
    __tablename__ = "setting_values"

    param: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    param_value: Mapped[str] = mapped_column(String(255), nullable=False)

    def __iter__(self):
        yield from {
            "param": self.param,
            "param_value": self.param_value,
        }.items()
