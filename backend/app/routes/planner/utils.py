import os
import time
from random import random

import requests
from geopy import Point
from geopy.distance import geodesic
from sqlalchemy import select
import geopy
from app.db import async_session_maker
from app.routes.planner.constants import graphhopper_route_base_url, graphhopper_locations_base_url, VEHICLE_TYPES
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


def compute_required_power(types, t, n_pass, cd_area, speed, weight_kg, eta, front_area, mu_r):
    alpha, beta, offset = get_hvac_parameters(types, t, n_pass)
    p_hvac = 0
    if t < 10:
        p_hvac = (alpha * (10 - t) + offset) * (1 - beta * n_pass)
    if 10 <= t < 16:
        p_hvac = (alpha * (16 - t) + offset) * (1 - beta * n_pass)
    if 16 <= t < 21:
        p_hvac = (alpha * (21 - t) + offset)
    if 21 <= t < 26:
        p_hvac = (alpha * (t - 21) + offset)
    if 26 <= t < 30:
        p_hvac = (alpha * (t - 25) + offset) * (1 + beta * n_pass)
    if 30 <= t:
        p_hvac = (alpha * (t - 26) + offset) * (1 + beta * n_pass)
    ro = 1.225
    g = 9.81
    f_aero = 0.5 * ro * cd_area * front_area * speed * speed
    f_roll = mu_r * weight_kg * g
    f_total = f_aero + f_roll
    power = f_total * speed + p_hvac
    return power / eta


def get_hvac_parameters(types, t, n_pass):
    alpha, beta, offset = 0, 0, 0
    if types == VEHICLE_TYPES["type1"]:
        if t < 10:
            alpha, beta, offset = 280, 0.05, 2010
        if 10 <= t < 16:
            alpha, beta, offset = 200, 0.03, 810
        if 16 <= t < 21:
            alpha, beta, offset = 150, 0, 60
        if 21 <= t < 26:
            alpha, beta, offset = 150, 0, 60
        if 26 <= t < 30:
            alpha, beta, offset = 190, 0.075, 660
        if 30 <= t:
            alpha, beta, offset = 240, 0.11, 1420

    if types == VEHICLE_TYPES["type2"]:
        if t < 10:
            alpha, beta, offset = 190, 0.05, 1500
        if 10 <= t < 16:
            alpha, beta, offset = 110, 0.03, 700
        if 16 <= t < 21:
            alpha, beta, offset = 85, 0, 0
        if 21 <= t < 26:
            alpha, beta, offset = 85, 0, 0
        if 26 <= t < 30:
            alpha, beta, offset = 167, 0.075, 660
        if 30 <= t:
            alpha, beta, offset = 240, 0.11, 1420

    if types == VEHICLE_TYPES["type3"]:
        if t < 10:
            alpha, beta, offset = 247, 0.05, 1950
        if 10 <= t < 16:
            alpha, beta, offset = 143, 0.03, 1053
        if 16 <= t < 21:
            alpha, beta, offset = 110.5, 0, 0
        if 21 <= t < 26:
            alpha, beta, offset = 110.5, 0, 0
        if 26 <= t < 30:
            alpha, beta, offset = 217.1, 0.075, 858
        if 30 <= t:
            alpha, beta, offset = 312, 0.11, 1846
    return alpha, beta, offset


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
            #add type and energy_usable field
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


def max_distance(t, n_pass, soc0, soc_min, soh, k, energyUsable, vehicle="ciao") -> float:
    #get parameters from vehicle parameter
    parameters = {
        "types": "sedan",
        "weight_kg": 1500.0,
        "cd_area": 0.32,
        "eta": 0.85,
        "front_area": 2.2,
        "mu_r": 0.01,
        "t": t,
        "n_pass": n_pass
    }
    energy_available = energyUsable * ((soc0 - soc_min) * soh * k) / 0.8 * 3.6e6
    total_distance = 0
    actual_speed = 0
    flag = True
    while energy_available > 0 and flag:
        next_speed = driverMaxSpeed(k)
        acc = next_speed - actual_speed
        acc = max(min(acc, driverMaxAcc(k)), -4.5)
        acc += random()
        p_batt = compute_required_power(**parameters, speed=actual_speed)
        energy_available -= p_batt
        if energy_available <= 0:
            flag = False
            break
        actual_speed += acc
        total_distance += actual_speed
        time.sleep(0.5)
    return total_distance


def swap_coordinates(route):
    return [[point[1], point[0]] for point in route]