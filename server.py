import uvicorn
from fastapi import FastAPI
from app.core.rdb import db_engine
from app.exceptions import register_exception_handler
from app.routers.home import home_route
from app.routers.users import user_route
from app.settings.base import HOST, PORT


def create_app() -> FastAPI:
    app = FastAPI()
    db_engine.init()
    app.include_router(user_route)
    app.include_router(home_route)
    register_exception_handler(app)
    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host=HOST, port=PORT)
