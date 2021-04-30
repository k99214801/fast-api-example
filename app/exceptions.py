from http import HTTPStatus
import logging

from fastapi import Request
from fastapi.responses import JSONResponse


class ServerException(Exception):
    def __init__(self, error_code, message, exc_detail=""):
        self._error_code = error_code
        self._message = message
        self._exc_detail = exc_detail

    @property
    def exc_detail(self):
        return self._exc_detail

    def to_dict(self):
        return {"error_code": self._error_code, "message": self._message}


class BadRequestException(ServerException):
    error_code = 100
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message):
        ServerException.__init__(self, BadRequestException.error_code, message)


class ConflictUserException(ServerException):
    error_code = 101
    status_code = HTTPStatus.CONFLICT

    def __init__(self, **kwargs):
        ServerException.__init__(self, ConflictUserException.error_code, **kwargs)


class NotFoundUserException(ServerException):
    error_code = 102
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, **kwargs):
        ServerException.__init__(self, NotFoundUserException.error_code, **kwargs)


class NotFoundSessionException(ServerException):
    error_code = 103
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, **kwargs):
        ServerException.__init__(self, NotFoundSessionException.error_code, **kwargs)


class InternalServerException(ServerException):
    error_code = 500
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, **kwargs):
        ServerException.__init__(self, InternalServerException.error_code, **kwargs)


def register_exception_handler(app):
    @app.exception_handler(InternalServerException)
    async def internal_exception_handler(request: Request, exc: InternalServerException):
        logging.error(exc.exc_detail)
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        logging.error(exc.exc_detail)
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(ConflictUserException)
    async def conflict_user_exception_handler(
        request: Request, exc: ConflictUserException
    ):
        logging.error(exc.exc_detail)
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(NotFoundUserException)
    async def not_found_user_exception_handler(
        request: Request, exc: NotFoundUserException
    ):
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(NotFoundSessionException)
    async def not_found_user_exception_handler(
        request: Request, exc: NotFoundSessionException
    ):
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
