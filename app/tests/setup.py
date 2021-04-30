import unittest
from fastapi.testclient import TestClient
from server import create_app
from app.core.rdb import db_engine

client = TestClient(create_app())


class BaseTestGroup(unittest.TestCase):
    active_user_id = 'active_user'
    leave_user_id = 'leave_user'
    password = '12test#$'

    @staticmethod
    def truncate_tables():
        conn = db_engine.get_engine('tests').connect()
        conn.execute(f'TRUNCATE TABLE users.users;')
        conn.execute(f'TRUNCATE TABLE users.sessions;')

    def setUp(self) -> None:
        BaseTestGroup.truncate_tables()
        self.initialize_data()

    def tearDown(self) -> None:
        BaseTestGroup.truncate_tables()

    def initialize_data(self):
        pass
