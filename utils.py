from aiogram.client.bot import Bot
from difflib import SequenceMatcher

from config import Config
from database import Database


async def check_spam(
        *,
        msg_text: str,
        config: Config,
        database: Database,
) -> bool:
    messages = await database.get_spam_msgs()
    for message in messages:
        similarity_ratio = SequenceMatcher(None, msg_text, message).ratio()
        if similarity_ratio >= config.threshold:
            return True
    return False


async def kick_user_from_chat(
        *,
        bot: Bot,
        chat_id: int,
        user_id: int,
        msg_id: int,
) -> None:
    await bot.delete_message(chat_id=chat_id, message_id=msg_id)
    await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
    await bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
