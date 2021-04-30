from abc import ABCMeta, abstractmethod
import secrets
from app.core.rdb import transaction
from app.exceptions import InternalServerException
from app.models.sessions import Sessions


class SessionKeyBaseMaker(metaclass=ABCMeta):
    @abstractmethod
    def make_session_key(self):
        pass


class SimpleSessionKeyMaker(SessionKeyBaseMaker):
    def make_session_key(self):
        return secrets.token_urlsafe(16)


class SessionService:
    @staticmethod
    def login(uid, ip):
        try:
            with transaction(commit=True) as db:
                session = Sessions(
                    user_rowid=uid,
                    ip=ip,
                    session_key=SimpleSessionKeyMaker().make_session_key(),
                )
                session.save(db)
            return {"session_key": session.session_key}
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))

    @staticmethod
    def logout(session_key):
        try:
            with transaction(commit=True) as db:
                Sessions(session_key=session_key).update_logout(db)
            return True
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))

    @staticmethod
    def retrieve(uid):
        try:
            with transaction() as db:
                sessions = Sessions(user_rowid=uid).find_by_user_rowid(db)

                result = []
                for session in sessions:
                    result.append(
                        {name: getattr(session, name) for name in session._fields}
                    )

                return result
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))
