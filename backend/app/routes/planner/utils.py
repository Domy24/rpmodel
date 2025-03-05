import os

from sqlalchemy import select

from app.db import async_session_maker
from app.routes.planner.constants import graphhopper_route_base_url
from app.vehicles.models import Vehicle


default_speed = 30
key = os.getenv("GRAPHHOPPER_SECRET_KEY")


def route_endpoint(start: tuple, end: tuple):
    start = f"{str(start[0])},{str(start[1])}"
    end = f"{str(end[0])},{str(end[1])}"
    return (f"{graphhopper_route_base_url}"
            f"&point={start}&point={end}"
            f"&profile=car"
            f"&key={key}"
            f"&type=json"
            f"&weighting=fastest"
            f"&details=max_speed"
            )


def calculate_speed_per_position(speeds, total_points):
    speed_per_position = [default_speed] * total_points
    for segment in speeds:
        start, end, max_speed = segment
        for i in range(start, end):
            if max_speed is not None:
                speed_per_position[i] = max_speed

    return speed_per_position


def driverMaxSpeed(k):
    if k == 0.9:
        return 90/3.6
    if k == 0.6:
        return 144/3.6
    if k == 0.5:
        return 180/3.6


def driverMaxAcc(k):
    if k == 0.9:
        return 1
    if k == 0.6:
        return 2.5
    if k == 0.5:
        return 9


def compute_required_power(cd_area, speed, weight_kg, eta, front_area, mu_r):
    ro = 1.225
    g = 9.81
    f_aero = 0.5 * ro * cd_area * front_area * speed * speed
    f_roll = mu_r * weight_kg * g
    f_total = f_aero + f_roll
    power = f_total * speed
    return power / eta


async def get_vehicle_parameters(vehicle) -> dict:
    AsyncSessionLocal = async_session_maker
    async with AsyncSessionLocal() as session:
        results = await session.execute(select(Vehicle).where(Vehicle.model == vehicle))
        model = results.scalar_one()
        return {
            "weight_kg": model.weight_kg,
            "cd_area": model.cd_area,
            "front_area": model.front_area,
            "eta": model.motor_efficiency,
            "mu_r": model.mu_r
        }

