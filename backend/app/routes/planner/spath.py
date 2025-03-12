# given two points (lat, lon) return shortest path
# the path is composed by a list of (lat, lon) couple
import requests
import polyline

from .constants import graphhopper_locations_base_url
from .utils import *

key = os.getenv("GRAPHHOPPER_SECRET_KEY")


def shortest_path(start, end) -> list[dict]:
    if not isinstance(start, tuple):
        start = from_name_to_lat_lng(start)
    if not isinstance(end, tuple):
        end = from_name_to_lat_lng(end)
    response = requests.get(url=route_endpoint(start, end))
    data = response.json()
    if response.status_code == 200:
        if data["paths"][0]["distance"] > 0:
            speeds = data["paths"][0]["details"]["max_speed"]
            total_points = speeds[-1][1]
            speed_per_point = calculate_speed_per_position(speeds, total_points)
            points = polyline.decode(data["paths"][0]["points"])
            edges = [{"point": point, "speed": (speed / 3.6)} for point, speed in zip(points, speed_per_point)]
            if points and len(points) > 0:
                return edges
            return []
    return []