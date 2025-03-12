from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session_maker
from app.routes.serializers import Route, RouteSegments
from app.routes.service.service import RouteService
from app.users.auth import fastapi_users
from app.users.models import User

router = APIRouter()


async def get_route_service() -> RouteService:
    async with async_session_maker() as session:
        yield RouteService(session)


@router.post("/route", response_model=RouteSegments)
async def get_best_route(route: Route, service: RouteService = Depends(get_route_service)):
    parameters = {
        "soc0": 0.9,
        "soc_min": 0.4,
        "soh": 0.9,
        "k": 0.5,
        "energyUsable": 90,
        "t": 11,
        "n_pass": 3
    }
    result = await service.get_best_route(route.start, route.end, parameters)
    if len(result["segments"]) == 0 and len(result["stations"]) == 0:
        return RouteSegments(detail="Route not found.")
    return RouteSegments(segments=result["segments"], stations=result["stations"])


@router.get("/users/me/routes", response_model=list)
async def get_user_routes(user: User = Depends(fastapi_users.current_user()),
                          service: RouteService = Depends(get_route_service)):
    if user:
        routes = await service.get_user_routes(user.id)
        return [{"start": r.start, "end": r.end, "id": r.id} for r in routes]
    return []


@router.post("/users/me/routes")
async def add_user_route(segments: RouteSegments, route: Route, user: User = Depends(fastapi_users.current_user()),
                         service: RouteService = Depends(get_route_service)):
    if user:
        await service.add_user_route(route.start, route.end, segments.segments, user.id)


@router.get("/users/me/routes/{route_id}", response_model=dict)
async def get_user_route(route_id: int, user: User = Depends(fastapi_users.current_user()),
                         service: RouteService = Depends(get_route_service)):
    if user:
        route = await service.get_route_by_id(route_id)
        if route:
            return {"segments": route.edges, "start": route.start, "end": route.end}
        else:
            return {"details": "No such route"}

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
