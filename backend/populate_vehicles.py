from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import count, func

from app.base import Base
from app.vehicles.models import Vehicle
from app.db import engine, async_session_maker

AsyncSessionLocal = async_session_maker


async def populate_vehicle_data(session: AsyncSession):
    vehicles_data = [

        {
            "model": "Tesla Model S",
            "vtype": "Gran Turismo Sedan",
            "weight_kg": 2000,
            "cd_area": 0.24,
            "velocity_kmh": 120,
            "motor_efficiency": 0.9,
            "mu_r": 0.012,
            "front_area": 2.34,
            "energy_usable": 90
        },
        {
            "model": "Porsche Taycan",
            "vtype": "Gran Turismo Sedan",
            "weight_kg": 2300,
            "cd_area": 0.22,
            "velocity_kmh": 140,
            "motor_efficiency": 0.92,
            "mu_r": 0.011,
            "front_area": 2.38,
            "energy_usable": 90
        },
        {
            "model": "Lucid Air",
            "vtype": "Gran Turismo Sedan",
            "weight_kg": 2100,
            "cd_area": 0.21,
            "velocity_kmh": 130,
            "motor_efficiency": 0.93,
            "mu_r": 0.0115,
            "front_area": 2.4,
            "energy_usable": 90
        },

        {
            "model": "Fiat 500e",
            "vtype": "City Car",
            "weight_kg": 1200,
            "cd_area": 0.28,
            "velocity_kmh": 80,
            "motor_efficiency": 0.85,
            "mu_r": 0.013,
            "front_area": 2.05,
            "energy_usable": 30
        },
        {
            "model": "Honda e",
            "vtype": "City Car",
            "weight_kg": 1400,
            "cd_area": 0.30,
            "velocity_kmh": 90,
            "motor_efficiency": 0.87,
            "mu_r": 0.0135,
            "front_area": 2.1,
            "energy_usable": 30
        },
        {
            "model": "Mini Cooper SE",
            "vtype": "City Car",
            "weight_kg": 1450,
            "cd_area": 0.29,
            "velocity_kmh": 100,
            "motor_efficiency": 0.86,
            "mu_r": 0.013,
            "front_area": 2.15,
            "energy_usable": 30
        },
        # Small SUV
        {
            "model": "Hyundai Kona Electric",
            "vtype": "Small SUV",
            "weight_kg": 1700,
            "cd_area": 0.27,
            "velocity_kmh": 100,
            "motor_efficiency": 0.88,
            "mu_r": 0.013,  #
            "front_area": 2.45,
            "energy_usable": 50
        },
        {
            "model": "Kia Niro EV",
            "vtype": "Small SUV",
            "weight_kg": 1800,
            "cd_area": 0.29,
            "velocity_kmh": 110,  # km/h
            "motor_efficiency": 0.89,
            "mu_r": 0.0135,
            "front_area": 2.5,
            "energy_usable": 50
        },
        {
            "model": "Mazda MX-30",
            "vtype": "Small SUV",
            "weight_kg": 1650,
            "cd_area": 0.30,
            "velocity_kmh": 95,
            "motor_efficiency": 0.86,
            "mu_r": 0.0138,
            "front_area": 2.6,
            "energy_usable": 50
        }
    ]

    result = await session.execute(select(func.count()).select_from(Vehicle))
    count = result.scalar()

    if count == 0:
        for vehicle_data in vehicles_data:
            velocity_mps = vehicle_data["velocity_kmh"] / 3.6  # Convert velocity to m/s
            vehicle = Vehicle(
                model=vehicle_data["model"],
                weight_kg=vehicle_data["weight_kg"],
                cd_area=vehicle_data["cd_area"],
                velocity_mps=velocity_mps,
                motor_efficiency=vehicle_data["motor_efficiency"],
                mu_r=vehicle_data["mu_r"],
                front_area=vehicle_data["front_area"],
                vtype=vehicle_data["vtype"],
                energy_usable=vehicle_data["energy_usable"]
            )
            session.add(vehicle)
        await session.commit()


async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        await populate_vehicle_data(session)
