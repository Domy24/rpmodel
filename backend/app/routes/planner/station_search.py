import math

from geopy.distance import geodesic
import polyline
import requests
import os

from app.routes.planner.models import Path
from app.routes.planner.spath import shortest_path
from app.routes.planner.utils import calculate_distance, find_common_subsequences, convert_from_point_to_edges, compute_k_point, divide_and_extract

KEY = os.getenv("OCM_SECRET_KEY")
from app.routes.planner.constants import ocm_base_url, MAX_DISTANCE, MIN_DISTANCE, MAX_STATIONS, MAX_RESULTS, DISTANCE, \
    COUNTRY_ID_LIST


async def evaluate_station_to_end(k, baseline, end, parameters):
    stations = await station_search(baseline, end, k)
    best_station = {"name": "not_a_station"}
    best_station_point = best_route = None
    for station in stations:
        points = shortest_path((station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]), end)
        route = Path(points=points)
        feasible = await route.is_feasible(**parameters)
        if compute_reward_fcn(baseline, station, end=end) > compute_reward_fcn(baseline, best_station, end=end) and feasible:
            best_station_point = (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])
            best_route = convert_from_point_to_edges(points)
    return best_station_point, best_route


async def evaluate_start_to_station(k, baseline, start, parameters):
    stations = await station_search(baseline, start, k)
    best_station = {"name": "not_a_station"}
    best_station_point = best_route = None
    for station in stations:
        points = shortest_path(start, (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]))
        route = Path(points=points)
        feasible = await route.is_feasible(**parameters)
        if compute_reward_fcn(baseline, station, start=start) > compute_reward_fcn(baseline, best_station, start=start) and feasible:
            best_station_point = (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])
            best_route = convert_from_point_to_edges(points)
    return best_station_point, best_route


async def station_search(baseline, point: tuple, k):
    l = convert_from_point_to_edges(baseline)
    r = divide_and_extract(l, k)
    line = polyline.encode(r)

    params = {
        "output": "json",
        "countrycode": COUNTRY_ID_LIST,
        "maxresults": MAX_RESULTS,
        "polyline": line,
        "distance": DISTANCE,
        "distanceunit": "km",
        "key": KEY
    }

    try:
        response = requests.get(ocm_base_url, params=params)
        data = response.json()
        stations = stations_pruning(baseline, data, point)
        return stations
    except Exception as e:
        raise Exception(str(e))


def compute_reward_fcn(baseline: list, station, start=None, end=None):
    if "name" in station:
        return float("-inf")
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


def stations_pruning(baseline, stations, point):
    length = calculate_distance(convert_from_point_to_edges(baseline))/1000
    pruned_stations = []
    for station in stations:
        distance = geodesic(point, (station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"])).kilometers
        if MIN_DISTANCE(length) < distance <= MAX_DISTANCE(length) and len(pruned_stations) <= MAX_STATIONS:
            pruned_stations.append(station)
    return pruned_stations
