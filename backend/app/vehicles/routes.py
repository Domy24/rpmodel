from fastapi import APIRouter, Depends

from app.db import async_session_maker
from app.users.auth import fastapi_users
from app.users.models import User
from app.vehicles.serializers import VehicleList, Vehicle
from app.vehicles.service.service import VehicleService

router = APIRouter()


async def get_vehicle_service() -> VehicleService:
    async with async_session_maker() as session:
        yield VehicleService(session)


@router.get("/vehicles", response_model=VehicleList)
async def get_all_vehicles(
        user: User = Depends(fastapi_users.current_user()),
        service: VehicleService = Depends(get_vehicle_service)
):
    vehicles = await service.get_vehicles()
    l = []
    for vehicle in vehicles:
        v = Vehicle(
            model=vehicle.model,
            weight_kg=vehicle.weight_kg,
            cd_area=vehicle.cd_area,
            velocity_mps=vehicle.velocity_mps,
            motor_efficiency=vehicle.motor_efficiency,
            front_area=vehicle.front_area,
            mu_r=vehicle.mu_r,
            vtype=vehicle.vtype,
            energy_usable=vehicle.energy_usable
        )
        l.append(v)
    return VehicleList(vehicles=l)

@router.post("/vehicles")
async def create_vehicle(
        vehicle : Vehicle,
        user: User = Depends(fastapi_users.current_user()),
        service: VehicleService = Depends(get_vehicle_service)
        ):
    return await service.create_vehicle(vehicle)