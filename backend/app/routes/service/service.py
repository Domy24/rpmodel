from sqlalchemy import UUID

from app.routes.planner.bidirectional_search import route_planner
from app.routes.repository.repository import RouteRepository

class RouteService:
    def __init__(self, session):
        self.dal = RouteRepository(session)

    async def get_best_route(self, start: str, end: str, parameters: dict):
        edges, stations = await route_planner(start, end, parameters)
        return {"segments": edges, "stations": stations}

    async def get_user_routes(self, user_id: UUID):
        return await self.dal.get_user_routes(user_id)

    async def get_route_by_id(self, route_id: int):
        return await self.dal.get_route_by_id(route_id)

    async def add_user_route(self, start: str, end: str, segments: list, user_id: UUID):
        return await self.dal.add_user_route(start, end, segments, user_id)
