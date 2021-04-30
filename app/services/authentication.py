import logging
from fastapi import Request
from app.core.rdb import transaction
from app.exceptions import BadRequestException, NotFoundSessionException
from app.models.sessions import Sessions


async def verify_session_key(req: Request):
    session_key = req.headers.get("x-session-key")
    try:
        if session_key is None:
            raise BadRequestException(message="x-session-key 값이 필요합니다")

        with transaction() as db:
            session = Sessions(session_key=session_key).find_by_session_key(db)
            setattr(req, "uid", int(session.user_rowid))

        return True
    except NotFoundSessionException:
        raise
