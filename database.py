from aiosqlite import connect, Connection, Cursor
from aiogram.loggers import logging
from asyncio import gather
from typing import Any, Optional


class Database:
    def __init__(self):
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

    async def _send(self, *, query: str, vargs: tuple[Any] = None) -> None:
        if self._cursor is None:
            await self.connect()
        try:
            await self._cursor.execute(sql=query, parameters=vargs)
        except Exception as e:
            self._logger.error(f"{query=} | {vargs=} | exception = {e}")

    async def _create_tables(self):
        query_1 = '''
        CREATE TABLE IF NOT EXISTS spam_messages(
        id INTEGER PRIMARY KEY,
        msg_text TEXT
        );
        '''
        query_2 = '''
        CREATE TABLE IF NOT EXISTS spam_words(
        id INTEGER PRIMARY KEY,
        word TEXT
        );
        '''
        await gather(self._send(query=query_1), self._send(query=query_2))
