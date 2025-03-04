import os
import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from .models import User
from .strategy import get_jwt_strategy
from .transport import bearer_transport
from .user_manager import get_user_manager

SECRET = os.getenv("BACKEND_AUTH_SECRET")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
