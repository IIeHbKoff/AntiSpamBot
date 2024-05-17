import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logging.handlers import RotatingFileHandler

from config import Config
from database import Database
from handlers import router
from utils import Utils

config = Config()
bot = Bot(token=config.bot_token)
database = Database(config=config)
scheduler = AsyncIOScheduler()
storage = MemoryStorage()
utils = Utils()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    handlers=[
        RotatingFileHandler(
            filename=config.logger_filename,
            maxBytes=config.logger_filesize,
            backupCount=config.logger_files_count,
        ),
    ]
)

dispatcher = Dispatcher(
    storage=storage,
    database=database,
    scheduler=scheduler,
    config=config,
    utils=utils,
)


@dispatcher.startup()
async def on_startup():
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
