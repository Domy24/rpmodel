from fastapi import APIRouter

from .planner.models import Path
from .serializers import Route
from ..routes.planner.spath import shortest_path

router = APIRouter()


@router.post("/route", response_model=Path)
async def generate_route(route: Route): #add try except for no route found
    sp = shortest_path(route.start, route.end)
    if len(sp) > 0:
        return Path(start=route.start, end=route.end, points=sp)
    return Path(start=route.start, end=route.end, points=[])
