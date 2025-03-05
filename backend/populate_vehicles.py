from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.vehicles.models import Vehicle
from app.db import engine, async_session_maker

AsyncSessionLocal = async_session_maker


async def populate_vehicles():
    async with AsyncSessionLocal() as session:
        vehicles_data = [
            {
                "model": "Tesla Model S",
                "weight_kg": 2000,
                "cd_area": 0.24,
                "velocity_kmh": 100,  # km/h
                "motor_efficiency": 0.9
            },
            {
                "model": "Nissan Leaf",
                "weight_kg": 1500,
                "cd_area": 0.25,
                "velocity_kmh": 90,  # km/h
                "motor_efficiency": 0.85
            },
            {
                "model": "BMW i3",
                "weight_kg": 1300,
                "cd_area": 0.23,
                "velocity_kmh": 120,  # km/h
                "motor_efficiency": 0.88
            }
        ]

        for vehicle_data in vehicles_data:
            velocity_mps = vehicle_data["velocity_kmh"] / 3.6
            vehicle = Vehicle(
                model=vehicle_data["model"],
                weight_kg=vehicle_data["weight_kg"],
                cd_area=vehicle_data["cd_area"],
                velocity_mps=velocity_mps,
                motor_efficiency=vehicle_data["motor_efficiency"]
            )
            session.add(vehicle)

    await session.commit()
