from abc import ABC

import sqlalchemy
from sqlalchemy import Table, Column, Integer, JSON, MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import Session, mapper

from avito.Item import Item


class Database(ABC):
    _engine: Engine
    _connection: Connection
    _session: Session
    _metadata: MetaData

    def __init__(self):
        self._connection = self._engine.connect()
        self._session = Session(bind=self._engine, expire_on_commit=False)
        self._metadata = sqlalchemy.MetaData()

        item_table_metadata = Table('item', self._metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('dictionary', JSON)
                                    )
        mapper(Item, item_table_metadata)
        self._metadata.create_all(self._engine)

    @property
    def session(self) -> Session:
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @session.deleter
    def session(self):
        self._session.close()

    def __del__(self):
        self._engine.dispose()
