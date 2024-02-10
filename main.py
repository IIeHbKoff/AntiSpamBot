import asyncio
import logging
from logging.handlers import RotatingFileHandler

import config

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import Database
from handlers import router

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
database = Database()
scheduler = AsyncIOScheduler()
dispatcher = Dispatcher(
    storage=MemoryStorage(),
    database=database,
    scheduler=scheduler,
)


@dispatcher.startup()
async def on_startup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                filename="anti_spam_bot.log",
                maxBytes=20000000,
                backupCount=5,
            ),
        ]
    )
    dispatcher.include_router(router)
    scheduler.start()
    await database.connect()
    await bot.delete_webhook(drop_pending_updates=True)


@dispatcher.shutdown()
async def on_shutdown():
    scheduler.shutdown()
    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(
        dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types()
        )
    )
