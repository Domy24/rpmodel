from sqlalchemy import select, UUID
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

    async def add_user_route(self, start: str, end: str, edges: list, user_id: UUID):
        new_route = RouteDB(start=start, end=end, edges=edges, user_id=user_id)
        self.session.add(new_route)
        await self.session.commit()
        return new_route