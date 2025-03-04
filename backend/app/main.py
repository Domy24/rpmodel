
import fastapi_users.router
from fastapi import FastAPI
from .users.auth import fastapi_users
from .users.auth import auth_backend
from .users.db import create_db_and_tables
from .routes import routes as route_routes
from .users.serializers import UserRead, UserCreate, UserUpdate

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)