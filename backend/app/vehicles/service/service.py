from app.vehicles.repository.repository import VehicleRepository
from app.vehicles.serializers import Vehicle


class VehicleService:
    def __init__(self, session):
        self.dal = VehicleRepository(session)

    async def get_vehicles(self):
        return await self.dal.get_vehicles()

    async def create_vehicle(self, vehicle_create: Vehicle):
        vehicle = await self.dal.add_vehicle(vehicle_create)
        return vehicle