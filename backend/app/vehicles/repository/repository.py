from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.vehicles.models import Vehicle
from app.vehicles.serializers import Vehicle as VehicleModel


class VehicleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_vehicles(self):
        results = await self.session.execute(select(Vehicle))
        vehicles = results.scalars().all()
        return vehicles

    async def add_vehicle(self, vehicle_create: VehicleModel):
        vehicle = Vehicle(
            model=vehicle_create.model,
            weight_kg=vehicle_create.weight_kg,
            cd_area=vehicle_create.cd_area,
            velocity_mps=vehicle_create.velocity_mps,
            motor_efficiency=vehicle_create.motor_efficiency,
            front_area=vehicle_create.front_area,
            mu_r=vehicle_create.mu_r,
            vtype=vehicle_create.vtype,
            energy_usable=vehicle_create.energy_usable
        )
        self.session.add(vehicle)
        await self.session.commit()
        return vehicle