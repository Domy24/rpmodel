# given two points (lat, lon) return shortest path
# the path is composed by a list of (lat, lon) couple
import requests
import polyline

from .constants import graphhopper_locations_base_url
from .utils import *

key = os.getenv("GRAPHHOPPER_SECRET_KEY")


def shortest_path(start, end) -> list[dict]:
    if type(start) is not tuple and type(end) is not tuple:
        params = {
            "q": start,
            "key": key
        }
        response = requests.get(graphhopper_locations_base_url, params=params)
        lat = response.json()["hits"][0]["point"]["lat"]
        lon = response.json()["hits"][0]["point"]["lng"]
        start = (lat, lon)
        params = {
            "q": end,
            "key": key
        }
        response = requests.get(graphhopper_locations_base_url, params=params)
        lat = response.json()["hits"][0]["point"]["lat"]
        lon = response.json()["hits"][0]["point"]["lng"]
        end = (lat, lon)
    response = requests.get(url=route_endpoint(start, end))
    data = response.json()
    if data["paths"][0]["distance"] > 0:
        speeds = data["paths"][0]["details"]["max_speed"]
        total_points = speeds[-1][1]
        speed_per_point = calculate_speed_per_position(speeds, total_points)
        points = polyline.decode(data["paths"][0]["points"])
        edges = [{"point": point, "speed": (speed / 3.6)} for point, speed in zip(points, speed_per_point)]
        if points and len(points) > 0:
            return edges
        return []
    else:
        return []
