from datetime import datetime
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, func, TypeDecorator, type_coerce, Index
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, BIGINT, TINYINT, DATETIME
from app.exceptions import NotFoundUserException, ConflictUserException

Base = declarative_base()


class SHA2Password(TypeDecorator):
    """Applies the SHA2 function to incoming passwords."""

    impl = CHAR(64)

    def bind_expression(self, bindvalue):
        return func.sha2(bindvalue, 256)

    class comparator_factory(CHAR.comparator_factory):
        def __eq__(self, other):
            local_pw = type_coerce(self.expr, CHAR)
            return local_pw == func.sha2(other, 256)


class Users(Base):
    __tablename__ = "users"

    ACTIVE = 0
    LEAVE = 1

    row_id = Column(BIGINT(unsigned=True), primary_key=True, comment="테이블 기본 아이디")
    id = Column(VARCHAR(length=255), comment="사용자 아이디")
    password = Column(SHA2Password(length=255), comment="사용자 비밀번호")
    leave = Column(TINYINT, default=0, comment="탈퇴 여부 1: 탈퇴")
    # https://stackoverflow.com/questions/64838259/reading-datetime-column-gives-detachedinstanceerror-after-session-is-closed
    last_login_dt = Column(DATETIME, nullable=True, comment="마지막 로그인 날짜")
    last_logout_dt = Column(DATETIME, nullable=True, comment="마지막 로그아웃 날짜")
    leave_dt = Column(DATETIME, nullable=True, comment="탈퇴 날짜")
    created_dt = Column(DATETIME, server_default=FetchedValue(), comment="생성 날짜(가입 날짜)")

    __table_args__ = (
        Index("idx_user_id_pw_leave", "id", "password", "leave"),
        Index("idx_user_id_leave", "id", "leave"),
    )

    __mapper_args__ = {"eager_defaults": True}

    class Meta:
        engine = "users"

    def to_dict(self):
        user = {
            "uid": self.row_id,
            "id": self.id,
            "created_at": self.created_dt.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if self.leave == Users.LEAVE:
            user.update({"leave_dt": self.leave_dt.strftime("%Y-%m-%d %H:%M:%S")})
        return user

    def save(self, db):
        if self.is_active(db):
            db.add(self)
        else:
            raise ConflictUserException(message=f"동일 아이디가 존재합니다")
        return self

    def is_active(self, db):
        user = (
            db.query(Users)
            .filter(Users.id == self.id, Users.leave == Users.ACTIVE)
            .one_or_none()
        )
        if user is not None:
            return False
        return True

    def find_by_id_password(self, db):
        user = (
            db.query(Users)
            .filter(
                Users.id == self.id,
                Users.password == self.password,
                Users.leave == Users.ACTIVE,
            )
            .one_or_none()
        )
        if user is None:
            raise NotFoundUserException(message=f"알 수 없는 회원 정보입니다")
        return user

    def login(self, db):
        db.query(Users).filter(Users.row_id == self.row_id).update(
            {"last_login_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        )
        return self

    def find_by_row_id(self, db):
        user = db.query(Users).filter(Users.row_id == self.row_id   ).one_or_none()
        if user is None:
            raise NotFoundUserException(message=f"알 수 없는 회원 정보입니다")
        return user

    def unregister(self, db):
        db.query(Users).filter(Users.row_id == self.row_id).update(
            {
                "leave": 1,
                "last_logout_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "leave_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    def logout(self, db):
        db.query(Users).filter(Users.row_id == self.row_id).update(
            {"last_logout_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        )
        return self
