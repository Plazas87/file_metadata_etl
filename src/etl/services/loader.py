"""Database loader module."""
from __future__ import annotations

import logging
from types import TracebackType
from typing import List, Optional, Type

import psycopg2
from psycopg2 import sql

from ..dtos import VideoMetaData
from ..services import ILoader

logger = logging.getLogger(__name__)


class DataLoader(ILoader[VideoMetaData]):  # pylint: disable=R0902
    """DataLoader class."""

    _host: str
    _port: int
    _database_name: str
    _password: str
    _user: str
    _table_name: str

    def __init__(  # pylint: disable=R0913
        self,
        host: str,
        port: int,
        password: str,
        database_name: str,
        user: str,
        table_name: str
    ) -> None:
        """Class constructor."""
        self._host = host
        self._port = port
        self._password = password
        self._database_name = database_name
        self._user = user
        self._table_name = table_name
        self._connection = None
        self._cursor = None

    def __enter__(self) -> DataLoader:
        """Set up the external resource."""
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
                database=self._database_name,
            )

        assert self._connection
        self._cursor = self._connection.cursor()

        return self

    def __exit__(
        self,
        exn_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> bool:
        """
        Execute the closing procedure for the external source.

        Args:
            exn_type (Optional[Type[BaseException]], optional): the exception class.
            exc_val (Optional[BaseException], optional): is the exception instance.
            exc_tb (Optional[TracebackType], optional): is the traceback object.

        Returns:
            bool: flag to configure whether an exception is caught or let it to propagate.
        """
        assert self._connection
        self._connection.commit()
        self._connection.close()


    def create_table(self) -> None:
        """Create the database table if does not exists."""
        logger.info("Setting up the database table: %s", self._table_name)
        
        check_table_query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)"
        self._cursor.execute(check_table_query, (self._table_name,))
        table_exists = self._cursor.fetchone()[0]

        if not table_exists:
            logger.info("Creating the table %s", self._table_name)
            create_table_query = sql.SQL("""
            CREATE TABLE {} (
                id SERIAL PRIMARY KEY,
                name VARCHAR,
                extension VARCHAR,
                size INTEGER,
                absolute_path VARCHAR
            )
            """).format(sql.Identifier(self._table_name))
            
            self._cursor.execute(create_table_query)

    def load(self, data: List[VideoMetaData]) -> None:
        """Insert the data into de database."""
        insert_query = """
        INSERT INTO {} (name, extension, size, absolute_path)
        VALUES (%s, %s, %s, %s)
        """
        for row in data:
            data = (row.name, row.extension, row.size, row.absolute_path)
            self._cursor.execute(sql.SQL(insert_query).format(sql.Identifier(self._table_name)), data)

