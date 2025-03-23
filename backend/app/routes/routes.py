from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from app.db import async_session_maker
from app.routes.serializers import Route, RouteSegments, RouteRequest, RouteUserList, RouteUserDetail
from app.routes.service.service import RouteService
from app.users.auth import fastapi_users
from app.users.models import User
router = APIRouter()


async def get_route_service() -> RouteService:
    async with async_session_maker() as session:
        yield RouteService(session)


@router.post("/route", response_model=RouteSegments)
async def get_best_route(
        route: RouteRequest,
        service: RouteService = Depends(get_route_service),
        user: User = Depends(fastapi_users.current_user())
):
    if user:
        result = await service.get_best_route(route.parameters.start, route.parameters.end, route.parameters.route_parameters, route.parameters.vehicle_parameters)
        if len(result["segments"]) == 0 and len(result["stations"]) == 0 and result["score"] == None:
            return RouteSegments(detail="Route not found.")
        return RouteSegments(segments=result["segments"], stations=result["stations"], score=result["score"])



@router.get("/users/me/routes", response_model=RouteUserList)
async def get_user_routes(
        user: User = Depends(fastapi_users.current_user()),
        service: RouteService = Depends(get_route_service)
):
    if user:
        results = await service.get_user_routes(user.id)
        routes = [Route(start=r.start, end=r.end, id=r.id) for r in results]
        return RouteUserList(routes=routes)


@router.post("/users/me/routes")
async def add_user_route(segments: RouteSegments, route: Route, user: User = Depends(fastapi_users.current_user()),
                         service: RouteService = Depends(get_route_service)):
    if user:
        try:
            await service.add_user_route(route.start, route.end, segments.segments, user.id, segments.stations)
            return {"success": True}
        except Exception as e:
            raise HTTPException(status_code=409, detail=str(e))


@router.get("/users/me/routes/{route_id}", response_model=RouteUserDetail)
async def get_user_route(route_id: int, user: User = Depends(fastapi_users.current_user()),
                         service: RouteService = Depends(get_route_service)):
    if user:
        route = await service.get_route_by_id(route_id)
        if route:
            return RouteUserDetail(start=route.start, end=route.end, route=RouteSegments(segments=route.edges, stations=route.stations))


