from datetime import datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import (
    IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command
)
from aiogram.loggers import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import Database
from fsm_contexts import CapchaState
from utils import check_bad_world, kick_user_from_chat

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("HelloWorld")


@router.message(Command("spam"))
async def spam_handler(msg: Message):
    logger.warning(f"SPAM - {msg.reply_to_message.text}")
    await msg.delete()
    await kick_user_from_chat(
        bot=msg.bot,
        user_id=msg.reply_to_message.from_user.id,
        chat_id=msg.chat.id,
        msg_id=msg.reply_to_message.message_id,
    )
    await msg.answer("Сообщение удалено")


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(
        event: ChatMemberUpdated,
        state: FSMContext,
        scheduler: AsyncIOScheduler,
):
    logger.info(f"NEW MEMBER - {event.new_chat_member.user.model_dump()}")
    msg = await event.answer(
        f"{event.new_chat_member.user.first_name} "
        f"Реши пример и пришли ответ в течение 60 сек "
        f"иначе ты будешь удалён из чата\n"
        f"2+2=?"
    )
    schedule_task_id = scheduler.add_job(
        kick_user_from_chat,
        trigger='date',
        run_date=datetime.now() + timedelta(seconds=60),
        kwargs={
            'bot': event.bot,
            "chat_id": event.chat.id,
            "user_id": event.new_chat_member.user.id,
            "msg_id": msg.message_id,
        }
    )
    await state.set_state(CapchaState.on_verification)
    await state.update_data(
        {
            "schedule_task_id": schedule_task_id,
            "right_answer": 4,
            "msg_id": msg.message_id,
        }
    )


@router.message(CapchaState.on_verification)
async def new_user_verification(
        msg: Message,
        state: FSMContext,
        scheduler: AsyncIOScheduler,
):
    data = await state.get_data()
    if msg.text.isdigit() and int(msg.text) == data["right_answer"]:
        scheduler.remove_job(job_id=data["schedule_task_id"].id)
        await msg.bot.delete_message(
            chat_id=msg.chat.id,
            message_id=data["msg_id"],
        )
        await msg.answer(
            text=f"{msg.from_user.first_name}, добро пожаловать в чат",
        )
    else:
        await kick_user_from_chat(
            bot=msg.bot,
            chat_id=msg.chat.id,
            user_id=msg.from_user.id,
            msg_id=data["msg_id"],
        )
    await msg.delete()


@router.message()
async def message_handler(
        msg: Message,
        database: Database,
):
    if msg.text is not None:
        if await check_bad_world(msg.text):
            logger.warning(f"BAD WORDS - {msg.text}")
            await msg.delete()
            await msg.answer("Сообщение удалено")
