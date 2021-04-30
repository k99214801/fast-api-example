from typing import List
from pydantic import BaseModel


class UserRegisterRequestData(BaseModel):
    id: str
    password: str


class UserRegisterResponseData(BaseModel):
    uid: str
    created_dt: str


class UserUnregisterResponseData(BaseModel):
    leave_dt: str


class UserLoginRequestData(BaseModel):
    id: str
    password: str


class UserLoginResponseData(BaseModel):
    uid: str
    session_key: str


class RetrieveSessionResponseData(BaseModel):
    session_key: str
    created_dt: str
    logout_dt: str


class RetrieveUserResponseData(BaseModel):
    uid: int
    id: str
    created_dt: str
    sessions: List[RetrieveSessionResponseData]
