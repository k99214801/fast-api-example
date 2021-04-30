from app.core.rdb import transaction
from app.exceptions import (
    ConflictUserException,
    NotFoundUserException,
    InternalServerException,
)
from app.models.users import Users


class UserService:
    @staticmethod
    def register(data):
        try:
            with transaction(commit=True) as db:
                user = Users(id=data.id, password=data.password)
                user.save(db)

            return {
                "uid": user.row_id,
                "created_at": user.created_dt.strftime("%Y-%m-%d %H:%M:%S"),
            }
        except ConflictUserException:
            raise
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))

    @staticmethod
    def unregister(uid):
        try:
            with transaction(commit=True) as db:
                user = Users(row_id=uid).find_by_row_id(db)
                if user.leave == Users.ACTIVE:
                    user.unregister(db)
            return {"uid": user.row_id, "leave_dt": user.leave_dt}

        except NotFoundUserException:
            raise
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))

    @staticmethod
    def login(data):
        try:
            with transaction(commit=True) as db:
                user = Users(id=data.id, password=data.password).find_by_id_password(db)
                user.login(db)
            return {"uid": user.row_id}
        except NotFoundUserException:
            raise
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))

    @staticmethod
    def logout(uid):
        try:
            with transaction(commit=True) as db:
                user = Users(row_id=uid).logout(db)
            return {"uid": user.row_id}
        except NotFoundUserException:
            raise
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))

    @staticmethod
    def retrieve(uid: int):
        try:
            with transaction() as db:
                user = Users(row_id=uid).find_by_row_id(db)
            return user.to_dict()
        except NotFoundUserException:
            raise
        except Exception as e:
            raise InternalServerException(message=f"서버 에러가 발생했습니다", exc_detail=str(e))
