import logging
from typing import List, Any

from psycopg2 import connect
from psycopg2._psycopg import cursor
from scrapy.utils.decorators import deprecated


@deprecated
class PostgreSQL:
    def __init__(self, dbname, user, password, host) -> None:
        logging.info(f"Creating PostgreSQL object with parameters {dbname} {user} ... {host} ")
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.db_connection = connect(dbname=dbname, user=user, password=password, host=host)

    def is_table_exists(self, table_name) -> bool:
        with self.db_connection.cursor() as cursor:
            cursor.execute(f"SELECT to_regclass('{table_name}');")
            is_exists = cursor.fetchone()[0] is not None
            logging.info(f"Table {table_name} exists {is_exists}")
            return is_exists

    def cursor(self) -> cursor:
        return self.db_connection.cursor()

    def select_items(self, table_name, is_detailed: bool, limit: int = "NULL") -> List[int]:
        with self.cursor() as cursor:
            cursor.execute(
                f"SELECT id FROM {table_name} WHERE is_detailed = {is_detailed} ORDER BY random() LIMIT {limit}")
            return [raw_id[0] for raw_id in cursor]

    def set_is_detailed(self, id: Any, is_detailed: bool, table_name: str) -> None:
        with self.cursor() as cursor:
            if type(id) is int or type(id) is str:
                cursor.execute(f"UPDATE {table_name} SET is_detailed = {is_detailed} WHERE id = {id}")
            elif type(id) is list:
                cursor.execute(f"UPDATE {table_name} SET is_detailed = {is_detailed} WHERE id IN {tuple(id)}")
            else:
                raise AttributeError("Invalid 'id' value type")
            cursor.connection.commit()

    def close(self) -> None:
        self.db_connection.close()
        assert self.db_connection.closed
        logging.info(f"PostgreSQL db_connection is closed")
