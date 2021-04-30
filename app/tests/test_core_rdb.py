from http import HTTPStatus
from app.core.rdb import transaction, DBEngines
from app.settings.base import DATABASE
from app.tests.setup import (
    client,
    BaseTestGroup
)


class ServerCoreRDBTest(BaseTestGroup):

    def initialize_data(self) -> None:
        pass

    def test_multiple_engine_init(self):
        engine_1 = DBEngines().init()
        engine_1.init()




