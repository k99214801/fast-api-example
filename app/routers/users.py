from http import HTTPStatus
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.serializers.users import (
    UserRegisterRequestData,
    UserRegisterResponseData,
    UserLoginRequestData,
    UserLoginResponseData,
    RetrieveUserResponseData,
)
from app.services.authentication import verify_session_key
from app.services.users import UserService
from app.services.session import SessionService

user_route = APIRouter(prefix="/v1/users")


@user_route.post("/")
async def register(
    data: UserRegisterRequestData, response_model=UserRegisterResponseData
):
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content=UserService.register(data)
    )


@user_route.delete("/", dependencies=[Depends(verify_session_key)])
async def unregister(request: Request, response_model=UserRegisterResponseData):
    user = UserService.unregister(request.uid)
    if user is not None:
        SessionService.logout(request.headers["x-session-key"])

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"leave_dt": user.get("leave_dt")}
    )


@user_route.put("/session")
async def login(
    data: UserLoginRequestData, request: Request, response_model=UserLoginResponseData
):
    user = UserService.login(data)
    session = SessionService.login(user.get("uid"), request.client.host)
    user.update({"session": session.get("session_key")})
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=user
    )


@user_route.delete("/session", dependencies=[Depends(verify_session_key)])
async def logout(request: Request):
    UserService.logout(request.uid)
    SessionService.logout(request.headers["x-session-key"])
    return JSONResponse(
        status_code=200
    )


@user_route.get("/{uid}")
async def retrieve(uid, response_model=RetrieveUserResponseData):
    user = UserService.retrieve(uid)
    sessions = SessionService.retrieve(uid)
    user.update({"sessions": sessions})
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=user
    )
