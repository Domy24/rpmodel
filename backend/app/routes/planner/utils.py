import os

import requests
from geopy import Point
from geopy.distance import geodesic
from sqlalchemy import select
import geopy
from app.db import async_session_maker
from app.routes.planner.constants import graphhopper_route_base_url, graphhopper_locations_base_url
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
        return 90 / 3.6
    if k == 0.6:
        return 144 / 3.6
    if k == 0.5:
        return 180 / 3.6


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


def find_common_subsequences(baseline, route):
    common_subsequences = []
    temp_sequence = []
    route_edges = convert_from_point_to_edges(route)
    baseline_edges = convert_from_point_to_edges(baseline)

    route_set = set(route_edges)

    for point in baseline_edges:
        if point in route_set:
            temp_sequence.append(point)
        else:
            if len(temp_sequence) >= 2:
                common_subsequences.append(temp_sequence)
            temp_sequence = []

    if len(temp_sequence) >= 2:
        common_subsequences.append(temp_sequence)

    return common_subsequences


def calculate_distance(sequence):
    # sequence_edges = []
    # for i in sequence:
    #     sequence_edges.append(i["point"])

    total_distance = 0
    for i in range(len(sequence) - 1):
        total_distance += geodesic(sequence[i], sequence[i + 1]).meters
    return total_distance


def convert_from_point_to_edges(point):
    # converts object of type {"point" : (lat, lon), "speed" : X} to list of points
    l = []
    for i in point:
        l.append(i["point"])
    return l


def compute_k_point(start, end, k):
    point = ((start[0] + end[0]) / k, (start[1] + end[1]) / k)
    return point


def divide_and_extract(baseline, k):
    indices = []
    n = len(baseline)
    step = n // (k + 1)
    indices.append(0)
    for i in range(1, k):
        indices.append(i * step)
    indices.append(n - 1)
    extracted_points = [baseline[i] for i in indices]

    return extracted_points


def from_name_to_lat_lng(name):
    params = {
        "q": name,
        "key": key
    }
    response = requests.get(graphhopper_locations_base_url, params=params)
    lat = response.json()["hits"][0]["point"]["lat"]
    lon = response.json()["hits"][0]["point"]["lng"]
    point = (lat, lon)
    return point
