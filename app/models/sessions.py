from datetime import datetime
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, func, Index
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME, TINYINT
from app.exceptions import NotFoundSessionException


Base = declarative_base()


class Sessions(Base):
    __tablename__ = "sessions"

    LOGIN = 0
    LOGOUT = 1

    row_id = Column(BIGINT(unsigned=True), primary_key=True, comment="테이블 기본 아이디")
    user_rowid = Column(BIGINT(unsigned=True), comment="사용자 테이블 로우 아이디")
    session_key = Column(VARCHAR(length=255), comment="세션 키")
    ip = Column(VARCHAR(length=20), comment="사용자 아이피")
    logout = Column(TINYINT, default=0, comment="로그아웃 여부")
    logout_dt = Column(DATETIME, nullable=True, comment="마지막 로그아웃 날짜")
    created_dt = Column(DATETIME, server_default=FetchedValue(), comment="생성 날짜(가입 날짜)")

    __table_args__ = (
        Index("idx_session_session_key_logout", "session_key", "logout"),
        Index("idx_session_user_rowid_created_dt", "user_rowid", "created_dt"),
    )

    class Meta:
        engine = "users"

    def save(self, db):
        if db:
            db.add(self)

    def find_by_session_key(self, db):
        session = (
            db.query(Sessions)
            .filter(Sessions.session_key == self.session_key, Sessions.logout == Sessions.LOGIN)
            .one_or_none()
        )
        if session is None:
            raise NotFoundSessionException(message="유효하지 않는 세션 정보 입니다")
        return session

    def update_logout(self, db):
        db.query(Sessions).filter(
            Sessions.session_key == self.session_key,
            Sessions.logout == Sessions.LOGIN,
        ).update(
            {
                "logout": Sessions.LOGOUT,
                "logout_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    def find_by_user_rowid(self, db):
        return (
            db.query(
                Sessions.session_key,
                func.date_format(Sessions.created_dt, "%Y-%m-%d %H:%i:%S").label(
                    "created_dt"
                ),
                func.date_format(Sessions.logout_dt, "%Y-%m-%d %H:%i:%S").label(
                    "logout_dt"
                ),
            )
            .filter(Sessions.user_rowid == self.user_rowid)
            .order_by(Sessions.row_id.desc())
            .all()
        )
