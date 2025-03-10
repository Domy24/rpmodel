# parameters = dict with soc0, soc_min, soh, k, energyUsable, vehicle
from app.routes.planner.models import Path
from app.routes.planner.spath import shortest_path
from .utils import *
from .station_search import *


async def route_planner(start, end, parameters):
    start_edge = from_name_to_lat_lng(start)
    end_edge = from_name_to_lat_lng(end)
    numstop = 0
    search_ended = False
    start_segment = []
    arrival_segment = []
    route = []
    stations = []
    while not search_ended:
        baseline = shortest_path(start_edge, end_edge)
        direct_route_edges = convert_from_point_to_edges(baseline)
        direct_route = Path(points=baseline)
        feasibility = await direct_route.is_feasible(**parameters)
        if feasibility:
            search_ended = True
            route = start_segment + direct_route_edges + arrival_segment
        else:
            k = 1
            best_station = best_edges = None
            numstop += 1
            if numstop % 2 == 1:
                while best_station is None:
                    best_station, best_edges = await evaluate_start_to_station(k, baseline=baseline, start=start_edge, parameters=parameters)
                    k *= 2
                start_edge = best_station
                start_segment += best_edges
                stations.append(best_station)
            else:
                while best_station is None:
                    best_station, best_edges = await evaluate_station_to_end(k, baseline=baseline, end=end_edge, parameters=parameters)
                    k *= 2
                end_edge = best_station
                arrival_segment = best_edges + arrival_segment
                stations.append(best_station)
    return route, stations
