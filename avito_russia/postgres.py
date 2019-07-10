import logging

from psycopg2 import connect
from psycopg2._psycopg import cursor


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
