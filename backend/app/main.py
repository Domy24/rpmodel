from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .users.auth import fastapi_users
from .users.auth import auth_backend
from .users.models import User
from .users.serializers import UserRead, UserCreate, UserUpdate
from .routes.routes import router
from app.routes.planner.utils import *

app = FastAPI()

origins = [
    "http://localhost:8080",
]

# Aggiungi il middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

