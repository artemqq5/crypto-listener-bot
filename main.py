import asyncio
import logging

import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from fastapi import FastAPI

from domain.handlers.user import main_user
from domain.middleware.AdminModeMiddleware import AdminModeMiddleware
from domain.middleware.IsRegisteredMiddleware import IsUserRegisteredMiddleware
from domain.middleware.LocaleManager import LocaleManager
from domain.use_cases.UpdateTaskTracking import UpdateTaskTracking

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(main_user.router)

default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=config.BOT_TOKEN, default=default_properties, timeout=60)

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await main()

    await bot.delete_webhook()

    # webhook_info = await bot.get_webhook_info()
    # if webhook_info.url != config.WEBHOOK_BASE_URL + config.WEBHOOK_PATH:
    await bot.set_webhook(
        url=config.WEBHOOK_BASE_URL + config.WEBHOOK_PATH, drop_pending_updates=True
    )
    asyncio.create_task(UpdateTaskTracking.start_all_checks())


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


@app.post(config.WEBHOOK_PATH)
async def receive_update(data: dict):
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


async def main():
    # logs
    logging.basicConfig(level=logging.INFO)

    # localization middleware
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="presentation/locales"
        ),  # Використовуємо абсолютний шлях
        default_locale="en",
        manager=LocaleManager(),
    )

    i18n_middleware.setup(dp)
    await i18n_middleware.core.startup()

    with i18n_middleware.use_context(locale="en") as i18n_context:
        UpdateTaskTracking.initialize(bot=bot, i18n=i18n_context)

    dp.message.outer_middleware(
        IsUserRegisteredMiddleware()
    )  # check if user not registered
    dp.callback_query.outer_middleware(
        IsUserRegisteredMiddleware()
    )  # check if user not registered

    dp.message.outer_middleware(AdminModeMiddleware())
    dp.callback_query.outer_middleware(AdminModeMiddleware())
