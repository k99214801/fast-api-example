import time
from datetime import datetime
from http import HTTPStatus
from app.core.rdb import transaction
from app.models.users import Users
from app.tests.setup import (
    client,
    BaseTestGroup
)


class ServerHomeTest(BaseTestGroup):

    def initialize_data(self) -> None:
        pass

    def test_retrieve(self):
        response = client.get(f"/")
        assert response.status_code == HTTPStatus.OK


