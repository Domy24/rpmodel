import math
import requests
import os
from app.routes.planner.spath import shortest_path
from app.routes.planner.utils import calculate_distance, find_common_subsequences, convert_from_point_to_edges

KEY = os.getenv("OCM_SECRET_KEY")
from app.routes.planner.constants import ocm_base_url, MIN_STATIONS


async def station_search(baseline, point: dict) -> dict:
    distance = 1
    max_results = 10

    params = {
        "output": "json",
        "countrycode": "IT",
        "maxresults": max_results,
        "latitude": point["lat"],
        "longitude": point["lon"],
        "distance": distance,
        "distanceunit": "KM",
        "key": KEY
    }

    response = requests.get(ocm_base_url, params=params)
    counter = 0
    best = {"details": "station not found"}
    while counter < MIN_STATIONS:
        if response.status_code == 200:
            data = response.json()
            counter += len(data)
            if counter > 0:
                best = data[0]
                for station in data[1:]:
                    try:
                        if compute_reward_fcn(baseline, distance, station, point) > compute_reward_fcn(baseline, distance, best,point):
                            best = station
                    except Exception as e:
                        counter -= 1
                        continue
            if counter < MIN_STATIONS:
                params["distance"] *= 2
                response = requests.get(ocm_base_url, params=params)
                data = response.json()
    return best


def compute_reward_fcn(baseline: list, distance, station, point):
    pkw = 0
    for connection in station["Connections"]:
        if connection["PowerKW"] is not None:
            if connection["PowerKW"] > pkw:
                pkw = connection["PowerKW"]
    if pkw == 0:
        pkw = 3.7

    route = shortest_path(start=(point["lat"], point["lon"]),
                          end=(station["AddressInfo"]["Latitude"], station["AddressInfo"]["Longitude"]))
    if len(route) == 0:
        raise Exception("shortest path not found")

    route_edges = convert_from_point_to_edges(route)
    baseline_points = convert_from_point_to_edges(baseline)
    sl = compute_shared_distance(baseline, route)

    print((math.pow((sl / calculate_distance(baseline_points)) / (1.001 - (sl / calculate_distance(route_edges))),
                     3) * pkw))
    return (math.pow((sl / calculate_distance(baseline_points)) / (1.001 - (sl / calculate_distance(route_edges))),
                     3) * pkw)


def compute_shared_distance(baseline, route):
    common_subsequences = find_common_subsequences(baseline, route)
    total_shared_distance = sum(calculate_distance(seq) for seq in common_subsequences)
    return total_shared_distance
