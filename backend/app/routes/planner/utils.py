import os

graphhopper_route_base_url = "https://graphhopper.com/api/1/route?"
graphhopper_locations_base_url = "https://graphhopper.com/api/1/geocode?"
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
        return 90
    if k == 0.6:
        return 144
    if k == 0.5:
        return 180

def driverMaxAcc(k):
    if k == 0.9:
        return 1
    if k == 0.6:
        return 2.5
    if k == 0.5:
        return 9