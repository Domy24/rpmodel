import os

graphhopper_route_base_url = "https://graphhopper.com/api/1/route?"
graphhopper_locations_base_url = "https://graphhopper.com/api/1/geocode?"

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
            )
