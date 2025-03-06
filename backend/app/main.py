from fastapi import FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.planner.models import Path
from app.routes.serializers import Route
from app.routes.planner.spath import shortest_path
from .db import async_session_maker
from .routes.planner.station_search import station_search, evaluate_station_to_end, evaluate_start_to_station
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


@app.get("/users")
async def get_users():
    AsyncSessionLocal = async_session_maker
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.all()
        list = []
        for user in users:
            us = user[0]
            list.append({
                "id": us.id,
                "email": us.email
            })
        return list


@app.post("/route_evaluation_to_end")
async def get_best_station(route: Route):
    baseline = shortest_path(eval(route.start), eval(route.end))
    parameters = {
        "soc0": 1,
        "soc_min": 0.3,
        "soh": 0.8,
        "k": 0.9,
        "energyUsable": 45
    }
    best_station = await evaluate_station_to_end(baseline, eval(route.end), parameters)
    return best_station

@app.post("/route_evaluation_from_start")
async def get_best_station(route: Route):
    baseline = shortest_path(eval(route.start), eval(route.end))
    parameters = {
        "soc0": 1,
        "soc_min": 0.3,
        "soh": 0.8,
        "k": 0.9,
        "energyUsable": 45
    }
    best_station = await evaluate_start_to_station(baseline, eval(route.end), parameters)
    return best_station