from fastapi import APIRouter, Depends
from sqlalchemy import select
from .models import Route as RouteDB
from .serializers import Route as Route
from .planner.bidirectional_search import route_planner
from .serializers import RouteSegments
from ..db import async_session_maker
from ..users.auth import fastapi_users
from ..users.models import User


router = APIRouter()


@router.post("/route", response_model=RouteSegments)
async def get_best_route(route: Route):
    parameters = {
        "soc0": 1,
        "soc_min": 0.3,
        "soh": 0.8,
        "k": 0.9,
        "energyUsable": 45
    }
    edges = await route_planner(route.start, route.end, parameters)
    route = RouteSegments(segments=edges)
    return route


@router.get("/users/me/routes", response_model=list)
async def get_user_routes(user: User = Depends(fastapi_users.current_user())):
    if user:
        AsyncSessionLocal = async_session_maker
        async with AsyncSessionLocal() as session:
            results = await session.execute(select(RouteDB).where(RouteDB.user_id == user.id))
            routes = results.all()
            names = []
            for route in routes:
                names.append({"start": route[0].start, "end": route[0].end, "id": route[0].id})
            return names
    return []

@router.post("/users/me/routes")
async def add_user_route(segments: RouteSegments, route: Route, user: User = Depends(fastapi_users.current_user())):
    if user:
        AsyncSessionLocal = async_session_maker
        async with AsyncSessionLocal() as session:
            row = RouteDB(start=route.start, end=route.end, edges=segments.segments, user_id=user.id)
            session.add(row)
            await session.commit()
            session.close()

@router.get("/users/me/routes/{route_id}", response_model=dict)
async def get_user_route(route_id: int, user: User = Depends(fastapi_users.current_user())):
    if user:
        AsyncSessionLocal = async_session_maker
        async with AsyncSessionLocal() as session:
            results = await session.execute(select(RouteDB).where(RouteDB.id == route_id))
            route = results.one()
            session.close()
            return {"segments": route[0].edges}
    return {}


# {
#     "segments": {
#         "segments": list
#     }
#
#     ,
#     "route": {
#         "start": str,
#         "end": str
#     }
#
# }
# segments list: [{"lat" : lat, "lon" : lon} ...]