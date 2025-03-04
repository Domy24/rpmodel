import os

from fastapi_users.authentication import JWTStrategy

SECRET = os.getenv("BACKEND_AUTH_SECRET")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
