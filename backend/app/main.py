from fastapi import FastAPI, Depends
from .users.auth import fastapi_users
from .users.auth import auth_backend
from .users.models import User
from .users.serializers import UserRead, UserCreate, UserUpdate
from .routes.routes import router
from app.routes.planner.utils import *

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



app.include_router(
    router
)

