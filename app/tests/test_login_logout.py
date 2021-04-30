import time
from datetime import datetime
from http import HTTPStatus
from app.core.rdb import transaction
from app.models.users import Users
from app.tests.setup import (
    client,
    BaseTestGroup
)


class UserLoginLogoutTest(BaseTestGroup):

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

    def test_active_login_out(self):
        """
        정상 로그인&로그아웃
        """
        response = client.put("/v1/users/session", json={
            'id': self.active_user_id,
            'password': self.password
        })
        assert response.status_code == HTTPStatus.OK

        response = response.json()
        assert response.get('session') is not None

        response = client.delete("/v1/users/session", headers={'x-session-key': response.get('session')})
        assert response.status_code == HTTPStatus.OK

    def test_leave_login(self):
        """
        탈퇴한 사용자 아이디로 로그인
        """
        response = client.put("/v1/users/session", json={
            'id': self.leave_user_id,
            'password': self.password
        })
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_unknown_logout(self):
        """
        알 수 없는 세션 키로 로그아웃
        """
        response = client.delete("/v1/users/session", headers={'x-session-key': 'unknown_session_key'})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_empty_session_header_logout(self):
        """
        헤더 값을 잊은 채로 로그아웃
        """
        response = client.delete("/v1/users/session")
        assert response.status_code == HTTPStatus.BAD_REQUEST
