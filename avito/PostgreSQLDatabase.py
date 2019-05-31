from sqlalchemy import create_engine

from avito.Database import Database


class PostgreSQLDatabase(Database):
    def __init__(self, db_url, echo=False):
        self._engine = create_engine(db_url, echo=echo)
        super().__init__()
