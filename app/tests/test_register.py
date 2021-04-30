import time
from datetime import datetime
from http import HTTPStatus
from app.core.rdb import transaction
from app.models.users import Users
from app.models.sessions import Sessions
from app.tests.setup import (
    client,
    BaseTestGroup
)


class UserRegisterUnRegisterTest(BaseTestGroup):

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

        response = client.put("/v1/users/session", json={
            'id': self.active_user_id,
            'password': self.password
        })
        assert response.status_code == HTTPStatus.OK

        response = response.json()
        assert response.get('session') is not None

        setattr(self, 'active_uid', active_user.row_id)
        setattr(self, 'active_session_key', response.get('session'))
        setattr(self, 'leave_uid', leave_user.row_id)

        # with transaction(commit=True) as db:
        #     session = Sessions(session_key=response.get('session')).find_by_session_key(db)
        #     session.user_rowid = 9999
        #     db.add(session)

    def test_active_register(self):
        """
        정상 회원 가입
        """
        response = client.post("/v1/users/", json={
            'id': 'register-test',
            'password': self.password
        })
        assert response.status_code == HTTPStatus.CREATED

    def test_conflict_register(self):
        """
        아이디 중복 확인
        """
        response = client.post("/v1/users/", json={
            'id': self.active_user_id,
            'password': self.password
        })
        assert response.status_code == HTTPStatus.CONFLICT

    def test_leave_register(self):
        """
        탈퇴한 아이디로 재 가입
        """
        response = client.post("/v1/users/", json={
            'id': self.leave_user_id,
            'password': self.password
        })
        assert response.status_code == HTTPStatus.CREATED


    def test_active_unregister(self):
        """
        정상 회원 탈퇴
        """
        response = client.delete("/v1/users/", headers={
            'x-session-key': self.active_session_key
        })
        assert response.status_code == HTTPStatus.OK

    def test_unknonw_session_key_unregister(self):
        """
        정상 회원 탈퇴
        """
        response = client.delete("/v1/users/", headers={
            'x-session-key': 'unknown_session_key'
        })
        assert response.status_code == HTTPStatus.NOT_FOUND
