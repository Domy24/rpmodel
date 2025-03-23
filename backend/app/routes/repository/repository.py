import json

from sqlalchemy import select, UUID, cast, String, ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from app.routes.models import Route as RouteDB


class RouteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_user_routes(self, user_id: UUID):
        results = await self.session.execute(select(RouteDB).where(RouteDB.user_id == user_id))
        return results.scalars().all()

    async def get_route_by_id(self, route_id: int):
        results = await self.session.execute(select(RouteDB).where(RouteDB.id == route_id))
        return results.scalar_one_or_none()

    async def add_user_route(self, start: str, end: str, edges: list, user_id: UUID, stations: list):
        new_route = RouteDB(start=start, end=end, edges=edges, user_id=user_id, stations=stations)
        edges_json = json.dumps(edges, sort_keys=True)
        stations_json = json.dumps(stations, sort_keys=True)
        existing_route = await self.session.execute(
            select(RouteDB).where(
                RouteDB.start == new_route.start,
                RouteDB.end == new_route.end,
                cast(RouteDB.edges, String) == edges_json,
                RouteDB.user_id == new_route.user_id,
                cast(RouteDB.stations, String) == stations_json,
            )
        )
        if existing_route.scalar_one_or_none():
            raise Exception("Object already exists")

        self.session.add(new_route)
        await self.session.commit()
        return new_route