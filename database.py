import logging

from aiosqlite import connect, Connection, Cursor
from asyncio import gather
from typing import Any, Optional

from config import Config


class Database:
    def __init__(self, config: Config):
        self._db: Optional[Connection] = None
        self._cursor: Optional[Cursor] = None
        self._logger = logging.getLogger(__name__)

    def __del__(self):
        self._db = None
        self._cursor = None

    async def connect(self) -> None:
        self._db: Connection = await connect("spam_db.sqlite")
        self._cursor: Cursor = await self._db.cursor()
        await self._create_tables()

    async def disconnect(self) -> None:
        if self._cursor is not None:
            await self._cursor.close()
        if self._db is not None:
            await self._db.close()

    async def send(self, *, query: str, vargs: tuple[Any] = None) -> None:
        if self._cursor is None:
            await self.connect()
        try:
            self._logger.info(f"{query=} | {vargs=}")
            await self._cursor.execute(sql=query, parameters=vargs)
            await self._db.commit()
        except Exception as e:
            self._logger.error(f"{query=} | {vargs=} | exception = {e}")

    async def read(self, *, query: str, vargs: tuple[Any] = None) -> Any:
        if self._cursor is None:
            await self.connect()
        try:
            self._logger.info(f"{query=} | {vargs=}")
            await self._cursor.execute(sql=query, parameters=vargs)
            result = await self._cursor.fetchall()
        except Exception as e:
            self._logger.error(f"{query=} | {vargs=} | exception = {e}")
            result = None
        return result

    async def _create_tables(self) -> None:
        query_1 = (
            'CREATE TABLE IF NOT EXISTS spam_messages'
            '('
            'id INTEGER PRIMARY KEY,'
            'msg_text TEXT'
            ');'
        )
        query_2 = (
            'CREATE TABLE IF NOT EXISTS spam_words'
            '('
            'id INTEGER PRIMARY KEY,'
            'word TEXT'
            ');'
        )
        query_3 = (
            'CREATE TABLE IF NOT EXISTS users'
            '('
            'tg_id INTEGER PRIMARY KEY,'
            'role text,'
            'msgs_count int not null default 0'
            ');'
        )
        await gather(
            self.send(query=query_1),
            self.send(query=query_2),
            self.send(query=query_3),
        )

    async def add_spam_message(self, *, message: str) -> None:
        query = 'INSERT INTO spam_messages (msg_text) VALUES (?);'
        await self.send(query=query, vargs=(message,))

    async def check_if_message_is_spam(self, *, message: str) -> bool:
        query = (
            'SELECT EXISTS(SELECT * FROM spam_messages WHERE msg_text = ?);'
        )
        result = await self.read(query=query, vargs=(message,))
        return bool(result[0][0])

    async def get_spam_msgs(self) -> list[str]:
        query = (
            'SELECT distinct msg_text from spam_messages;'
        )
        result = await self.read(query=query)
        return [res[0] for res in result]

    async def update_users_msgs_count(self, *, user_tg_id: int) -> None:
        query = (
            'INSERT INTO users (tg_id, msgs_count) VALUES (?, 1) '
            'ON CONFLICT (tg_id) DO UPDATE SET msgs_count = msgs_count + 1;'
        )
        await self.send(query=query, vargs=(user_tg_id,))
