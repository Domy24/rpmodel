from app.vehicles.repository.repository import VehicleRepository


class VehicleService:
    def __init__(self, session):
        self.dal = VehicleRepository(session)

    async def get_vehicles(self):
        return await self.dal.get_vehicles()
