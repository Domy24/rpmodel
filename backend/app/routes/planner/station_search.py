import math
import requests
import os

from app.routes.planner.models import Path
from app.routes.planner.spath import shortest_path
from app.routes.planner.utils import calculate_distance, find_common_subsequences, convert_from_point_to_edges, \
    compute_medium_point

KEY = os.getenv("OCM_SECRET_KEY")
from app.routes.planner.constants import ocm_base_url, MIN_STATIONS


async def evaluate_station_to_end(baseline, end, parameters):
    # parameters = dict with soc0, soc_min, soh, k, energyUsable, vehicle
    point = compute_medium_point(baseline[0]["point"], baseline[-1]["point"])
    distance = calculate_distance(convert_from_point_to_edges(baseline)) / 2
    stations = await station_search(baseline, point, distance)
    best_station = stations[0]  # check is_feasile for first element
    best_station_point = (stations[0]["AddressInfo"]["Latitude"], stations[0]["AddressInfo"]["Longitude"])
    best_route = convert_from_point_to_edges(shortest_path((best_station_point[0], best_station_point[1]),end))
    for station in stations[1:]:
        points = shortest_path((station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]), end)
        route = Path(points=points)
        feasible = await route.is_feasible(**parameters)
        if compute_reward_fcn(baseline, station, end=end) > compute_reward_fcn(baseline, best_station,
                                                                           end=end) and feasible:
            best_station_point = (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])
            best_route = convert_from_point_to_edges(points)
    return best_station_point, best_route


async def evaluate_start_to_station(baseline, start, parameters):
    # parameters = dict with soc0, soc_min, soh, k, energyUsable, vehicle
    point = compute_medium_point(baseline[0]["point"], baseline[-1]["point"])
    distance = calculate_distance(convert_from_point_to_edges(baseline)) / 2
    stations = await station_search(baseline, point, distance)
    best_station = stations[0] # check is_feasile for first element
    best_station_point = (stations[0]["AddressInfo"]["Latitude"], stations[0]["AddressInfo"]["Longitude"])
    best_route = convert_from_point_to_edges(shortest_path(start,(best_station_point[0], best_station_point[1])))
    for station in stations[1:]:
        points = shortest_path(start,(station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]))
        route = Path(points=points)
        feasible = await route.is_feasible(**parameters)
        if compute_reward_fcn(baseline, station, start=start) > compute_reward_fcn(baseline,
                                                                           best_station, start=start) and feasible:
            best_station_point = (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])
            best_route = convert_from_point_to_edges(points)
    return best_station_point, best_route

async def station_search(baseline, point: tuple, distance=None):
    distance = 1 if distance is None else distance
    max_results = 10

    params = {
        "output": "json",
        "countrycode": "IT",
        "maxresults": max_results,
        "latitude": point[0],
        "longitude": point[1],
        "distance": distance,
        "distanceunit": "KM",
        "key": KEY
    }
    counter = 0
    stations = []
    while counter < MIN_STATIONS:
        response = requests.get(ocm_base_url, params=params)
        data = response.json()
        stations += data
        counter += len(data)
        params["distance"] *= 2
    return stations


def compute_reward_fcn(baseline: list, station, start=None, end=None):
    pkw = 0
    for connection in station["Connections"]:
        if connection["PowerKW"] is not None:
            if connection["PowerKW"] > pkw:
                pkw = connection["PowerKW"]
    if pkw == 0:
        pkw = 3.7

    if start is not None:
        route = shortest_path(start=(start[0], start[1]),
                              end=(station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]))
        if len(route) == 0:
            raise Exception("shortest path not found")

        route_edges = convert_from_point_to_edges(route)
        baseline_points = convert_from_point_to_edges(baseline)
        sl = compute_shared_distance(baseline, route)

        return (math.pow((sl / calculate_distance(baseline_points)) / (1.001 - (sl / calculate_distance(route_edges))),
                         3) * pkw)
    elif end is not None:
        route = shortest_path(start=(station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]),
                              end=(end[0], end[1]))
        if len(route) == 0:
            raise Exception("shortest path not found")

        route_edges = convert_from_point_to_edges(route)
        baseline_points = convert_from_point_to_edges(baseline)
        sl = compute_shared_distance(baseline, route)

        return (math.pow((sl / calculate_distance(baseline_points)) / (1.001 - (sl / calculate_distance(route_edges))),
                         3) * pkw)


def compute_shared_distance(baseline, route):
    common_subsequences = find_common_subsequences(baseline, route)
    total_shared_distance = sum(calculate_distance(seq) for seq in common_subsequences)
    return total_shared_distance
