import math

import requests
import os

from app.routes.planner.spath import shortest_path

KEY = os.getenv("OCM_SECRET_KEY")
from app.routes.planner.constants import ocm_base_url, MIN_STATIONS


async def station_search(point: dict) -> dict:
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

    if response.status_code == 200:
        data = response.json()
        while len(data) < MIN_STATIONS:
            params["distance"] += 1
            response = requests.get(ocm_base_url, params=params)
            data = response.json()

        best = data[0]
        for station in data[1:]:
            if compute_reward_fcn(distance, station) > compute_reward_fcn(distance, best):
                best = station

        return best

def compute_reward_fcn(distance, station):
    pkw = 0
    for connection in station["Connections"]:
        if connection["PowerKW"] > pkw:
            pkw = connection["PowerKW"]


    return 1 / (math.pow(
        (station["AddressInfo"]["Distance"] / distance) / (1.001 - (station["AddressInfo"]["Distance"] / distance)), 3)*pkw)
