import time
from datetime import datetime
from http import HTTPStatus
from app.core.rdb import transaction
from app.models.users import Users
from app.tests.setup import (
    client,
    BaseTestGroup
)


class UserRetrieveTest(BaseTestGroup):

    def initialize_data(self) -> None:
        with transaction(commit=True) as db:
            # Active User
            active_user = Users(id=self.active_user_id, password=self.password).save(db)

            # Leave User
            leave_user = Users(
                id=self.leave_user_id,
                password=self.password,
                leave=Users.LEAVE,
                leave_dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')).save(db)

        setattr(self, 'active_uid', active_user.row_id)
        setattr(self, 'leave_uid', leave_user.row_id)

        for i in range(0, 2):
            response = client.put("/v1/users/session", json={
                'id': self.active_user_id,
                'password': self.password
            })
            assert response.status_code == HTTPStatus.OK
            # 테스트 메소드 수 만큼 setup 호출로 테스트 완료가 조금 걸린다
            time.sleep(1)

    def test_retrieve(self):
        response = client.get(f"/v1/users/{self.active_uid}")
        assert response.status_code == HTTPStatus.OK

        response = response.json()
        assert response.get('leave_dt') is None

    def test_retrieve_order_by_sessions(self):
        response = client.get(f"/v1/users/{self.active_uid}")
        assert response.status_code == HTTPStatus.OK

        response = response.json()
        sessions = response.get('sessions')

        assert len(sessions) == 2

        assert sessions[0].get('created_dt') > sessions[1].get('created_dt')

    def test_leave_retrieve(self):
        response = client.get(f"/v1/users/{self.leave_uid}")
        assert response.status_code == HTTPStatus.OK

        response = response.json()
        assert response.get('leave_dt') is not None

    def test_unknown_uid_retrieve(self):
        response = client.get(f"/v1/users/99026463829")
        assert response.status_code == HTTPStatus.NOT_FOUND

