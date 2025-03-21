from sqlalchemy import UUID
from urllib3.util.util import reraise

from app.routes.planner.bidirectional_search import route_planner
from app.routes.repository.repository import RouteRepository
from app.routes.serializers import VehicleParameters, EnvParameters


class RouteService:
    def __init__(self, session):
        self.dal = RouteRepository(session)

    async def get_best_route(self, start: str, end: str, route_parameters: EnvParameters, vehicle_parameters: VehicleParameters):
        edges, stations, score = await route_planner(start, end, route_parameters=route_parameters, vehicle_parameters=vehicle_parameters)
        return {"segments": edges, "stations": stations, "score": score}

    async def get_user_routes(self, user_id: UUID):
        return await self.dal.get_user_routes(user_id)

    async def get_route_by_id(self, route_id: int):
        return await self.dal.get_route_by_id(route_id)

    async def add_user_route(self, start: str, end: str, segments: list, user_id: UUID, stations: list):
        try:
            return await self.dal.add_user_route(start, end, segments, user_id, stations)
        except Exception as e:
            raise e
