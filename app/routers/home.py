from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse

home_route = APIRouter(prefix="")


@home_route.get("/")
async def home():
    return JSONResponse(status_code=HTTPStatus.OK, content={'message': 'Hello!! Server is Running'})
