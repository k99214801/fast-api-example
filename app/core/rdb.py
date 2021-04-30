from contextlib import contextmanager
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.settings.base import DATABASE


class DBEngines:
    def __init__(self):
        self._init = False
        self._engines = {}

    def init(self):
        if self._init:
            return self

        for name, data in DATABASE.items():
            opts = {
                "echo": data.get("echo", False),
                "pool_recycle": data.get("pool_recycle", -1),
                "pool_size": data.get("pool_size", 5),
                "max_overflow": data.get("max_overflow", 10),
            }
            try:
                self._engines[name] = create_engine(data.get("engine"), **opts)
            except Exception as e:
                logging.error(f"DBEngines: Failed to init, {e}")
                raise e

        self._init = True
        return self

    def get_engine(self, name):
        return self._engines.get(name)


db_engine = DBEngines()


class RDBSession(Session):
    def get_bind(self, mapper, clause=None):
        return db_engine.get_engine(mapper.class_.Meta.engine)


class TestSession(Session):
    def get_bind(self, mapper, clause=None):
        return db_engine.get_engine('tests')


session_maker = sessionmaker(class_=RDBSession, expire_on_commit=False)
test_session_maker = sessionmaker(class_=TestSession, expire_on_commit=False)


@contextmanager
def transaction(commit=False):
    session = session_maker()
    try:
        yield session
        if commit:
            session.commit()
    except:
        if commit:
            session.rollback()
        raise
    finally:
        session.close()
