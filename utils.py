from aiogram.client.bot import Bot


async def check_bad_world(message):
    bad_world_list = [
        'крипта', "криптовалют", "forex",
        "CLICK ON THE LINK TO JOIN",
        "для тестирования сети",
    ]
    bad_worlds_counter = 0
    for bad_world in bad_world_list:
        if bad_world in message:
            bad_worlds_counter += 1

    if bad_worlds_counter > 0:
        return True
    else:
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
    # await bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
