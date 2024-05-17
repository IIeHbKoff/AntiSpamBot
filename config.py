import os
import configparser
import logging


class Config:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = configparser.ConfigParser()
        self._config.read('config.ini')

    @property
    def bot_token(self) -> str:
        return self._config.get(
            "bot",
            "token",
            fallback=os.getenv("BOT_TOKEN"),
        )

    @property
    def db_engine(self) -> str:
        return self._config.get(
            "database",
            "engine",
            fallback="sqlite",
        )

    @property
    def db_host(self) -> str:
        return self._config.get(
            "database",
            "host",
            fallback=os.getenv("DB_HOST"),
        )

    @property
    def db_port(self) -> int:
        return self._config.getint(
            "database",
            "port",
            fallback=os.getenv("DB_PORT"),
        )

    @property
    def db_name(self) -> str:
        return self._config.get(
            "database",
            "db_name",
            fallback=os.getenv("DB_NAME"),
        )

    @property
    def db_username(self) -> str:
        return self._config.get(
            "database",
            "username",
            fallback=os.getenv("DB_USERNAME"),
        )

    @property
    def db_password(self) -> str:
        return self._config.get(
            "database",
            "password",
            fallback=os.getenv("DB_PASSWORD"),
        )

    @property
    def cache_engine(self) -> str:
        return self._config.get(
            "cache",
            "engine",
            fallback="memory",
        )

    @property
    def cache_host(self) -> str:
        return self._config.get(
            "cache",
            "host",
            fallback=os.getenv("CACHE_HOST"),
        )

    @property
    def cache_port(self) -> int:
        return self._config.getint(
            "cache",
            "port",
            fallback=os.getenv("CACHE_PORT"),
        )

    @property
    def cache_db_name(self) -> str:
        return self._config.get(
            "cache",
            "db_name",
            fallback=os.getenv("CACHE_NAME"),
        )

    @property
    def cache_username(self) -> str:
        return self._config.get(
            "cache",
            "username",
            fallback=os.getenv("CACHE_USERNAME"),
        )

    @property
    def cache_password(self) -> str:
        return self._config.get(
            "cache",
            "password",
            fallback=os.getenv("CACHE_PASSWORD"),
        )

    @property
    def logger_driver(self) -> str:
        return self._config.get(
            "logger",
            "driver",
            fallback="file",
        )

    @property
    def logger_filename(self) -> str:
        return self._config.get(
            "logger",
            "filename",
            fallback="bot.log",
        )

    @property
    def logger_filesize(self) -> int:
        data = self._config.get(
            "logger",
            "filesize",
            fallback="10 mb",
        )
        value = 10 * (2 ** 10)
        try:
            data = data.split(" ")
            if data[1] == "b":
                value = int(data[0])
            elif data[1] in ('kb', 'Kb', 'KB'):
                value = int(data[0]) * (2 ** 10)
            elif data[1] in ('mb', 'Mb', 'MB'):
                value = int(data[0]) * (2 ** 20)
            elif data[1] == ('gb', 'Gb', 'GB'):
                value = int(data[0]) * (2 ** 30)
        except (TypeError, ValueError) as e:
            self._logger.error(e)
        finally:
            return value

    @property
    def logger_files_count(self) -> int:
        return self._config.getint(
            "logger",
            "files_count",
            fallback=5,
        )

    @property
    def threshold(self) -> float:
        return self._config.getfloat(
            "spam_filter",
            "threshold",
            fallback=0.7,
        )

    @property
    def allow_to_ban(self) -> bool:
        return self._config.getboolean(
            "spam_filter",
            "allow_to_ban",
            fallback=False,
        )

    @property
    def answer_to_deleted_messages(self) -> bool:
        return self._config.getboolean(
            "spam_filter",
            "answer_to_deleted_messages",
            fallback=True,
        )
