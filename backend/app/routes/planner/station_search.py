import math

from geopy.distance import geodesic
import polyline
import requests
import os

from app.routes.planner.models import Path
from app.routes.planner.spath import shortest_path
from app.routes.planner.utils import calculate_distance, find_common_subsequences, convert_from_point_to_edges, \
    compute_k_point, divide_and_extract, swap_coordinates


from app.routes.planner.constants import ocm_base_url, MAX_DISTANCE, MIN_DISTANCE, MAX_STATIONS, MAX_RESULTS, DISTANCE, \
    COUNTRY_ID_LIST, MAX_ATTEMPTS, MAX_POINTS


async def evaluate_station_to_end(baseline, end, env_parameters, vehicle_parameters):
    stations = await station_search(baseline, end)
    best_station_point = best_route = None
    best_reward = float("-inf")
    for station in stations:
        actual_reward = compute_reward_fcn(baseline, station, end=end)
        if actual_reward > best_reward:
            points = shortest_path((station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]), end)
            route = Path(points=points)
            best_reward = actual_reward
            feasible = await route.is_feasible(**env_parameters, vehicle_parameters=vehicle_parameters)
            if feasible:
                best_station_point = (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])
                best_route = convert_from_point_to_edges(points)
    return best_station_point, best_route


async def evaluate_start_to_station(baseline, start, env_parameters, vehicle_parameters):
    stations = await station_search(baseline, start)
    best_station_point = best_route = None
    best_reward = float("-inf")
    for station in stations:
        actual_reward = compute_reward_fcn(baseline, station, start=start)
        if actual_reward > best_reward:
            points = shortest_path(start, (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]))
            route = Path(points=points)
            best_reward = actual_reward
            feasible = await route.is_feasible(**env_parameters, vehicle_parameters=vehicle_parameters)
            if feasible:
                best_station_point = (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])
                best_route = convert_from_point_to_edges(points)
    return best_station_point, best_route


async def station_search(baseline, point: tuple):
    l = convert_from_point_to_edges(baseline)
    r = divide_and_extract(l, MAX_POINTS)
    line = polyline.encode(r)

    params = {
        "output": "json",
        "countrycode": COUNTRY_ID_LIST,
        "maxresults": MAX_RESULTS,
        "polyline": line,
        "distance": DISTANCE,
        "distanceunit": "km",
    }
    counter = 1
    while counter < MAX_ATTEMPTS:
        try:
            response = requests.get(ocm_base_url, params=params)
            data = response.json()
            stations = stations_pruning(baseline, data, point, counter)
            return stations
        except Exception as e:
            params["distance"] *= 2
            params["maxresults"] *= 2
            counter += 1



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
            return float("-inf")

        route_edges = convert_from_point_to_edges(route)
        baseline_points = convert_from_point_to_edges(baseline)
        sl = compute_shared_distance(baseline, route)

        return (math.pow((sl / calculate_distance(baseline_points)) / (1.001 - (sl / calculate_distance(route_edges))),
                         3) * pkw)
    elif end is not None:
        route = shortest_path(start=(station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]),
                              end=(end[0], end[1]))
        if len(route) == 0:
            return float("-inf")

        route_edges = convert_from_point_to_edges(route)
        baseline_points = convert_from_point_to_edges(baseline)
        sl = compute_shared_distance(baseline, route)

        return (math.pow((sl / calculate_distance(baseline_points)) / (1.001 - (sl / calculate_distance(route_edges))),
                         3) * pkw)


def compute_shared_distance(baseline, route):
    common_subsequences = find_common_subsequences(baseline, route)
    total_shared_distance = sum(calculate_distance(seq) for seq in common_subsequences)
    return total_shared_distance


def stations_pruning(baseline, stations, point, k):
    length = calculate_distance(convert_from_point_to_edges(baseline))/1000
    pruned_stations = []
    for station in stations:
        distance = geodesic(point, (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])).kilometers
        if MIN_DISTANCE(length, k) < distance <= MAX_DISTANCE(length, k) and len(pruned_stations) <= MAX_STATIONS:
            pruned_stations.append(station)
    return pruned_stations
