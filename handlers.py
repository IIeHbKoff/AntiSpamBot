from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import (
    IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command
)
from aiogram.loggers import logging

from utils import check_bad_world, kick_user_from_chat

router = Router()
logger = logging.getLogger('handlers')


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("HelloWorld")


@router.message(Command("spam"))
async def spam_handler(msg: Message):
    logger.warning(f"SPAM - {msg.reply_to_message.text}")
    await msg.delete()
    await msg.reply_to_message.delete()
    await msg.answer("Сообщение удалено")
    await kick_user_from_chat(
        bot=msg.bot,
        user_id=msg.reply_to_message.from_user.id,
        chat_id=msg.chat.id,
    )


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):
    logger.info(f"NEW MEMBER - {event.new_chat_member.user.model_dump()}")
    await event.answer(
        text=f"Добро пожаловать в чат {event.new_chat_member.user.first_name}",
    )


@router.message()
async def message_handler(msg: Message):
    if msg.text is not None:
        if await check_bad_world(msg.text):
            logger.warning(f"BAD WORDS - {msg.text}")
            await msg.delete()
            await msg.answer("Сообщение удалено")
