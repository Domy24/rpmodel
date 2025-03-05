from fastapi import FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.planner.models import Path
from app.routes.serializers import Route
from app.routes.planner.spath import shortest_path
from .db import async_session_maker
from .routes.planner.station_search import station_search
from .users.auth import fastapi_users
from .users.auth import auth_backend
from .users.models import User
from .users.serializers import UserRead, UserCreate, UserUpdate
from .routes.routes import router
from .vehicles.models import Vehicle

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

# @app.get("/users")
# async def get_users():
#     AsyncSessionLocal = async_session_maker
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(select(User).where(User.id == "bcc9d017-02d1-4b16-b278-b61338420e98"))
#         users = result.all()
#         list = []
#         for user in users:
#             us = user[0]
#             list.append({
#                 "id": us.id,
#                 "email": us.email
#             })
#         return list
#

@app.post("/station")
async def get_station(point: dict) -> dict:
    sp = shortest_path(point["start"], point["end"])
    station = await station_search(sp, point)
    return station

