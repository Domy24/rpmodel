from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.vehicles.models import Vehicle


class VehicleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_vehicles(self):
        results = await self.session.execute(select(Vehicle))
        vehicles = results.scalars().all()
        return vehicles
