# parameters = dict with soc0, soc_min, soh, k, energyUsable, vehicle
from .constants import COVERAGE_LIMIT
from .utils import *
from .station_search import *
from ..serializers import EnvParameters, VehicleParameters


async def route_planner(start, end, vehicle_parameters: VehicleParameters, route_parameters: EnvParameters):
    try:
        start_edge = eval(start)
    except:
        start_edge = from_name_to_lat_lng(start)
    try:
        end_edge = eval(end)
    except:
        end_edge = from_name_to_lat_lng(end)
    numstop = 0
    search_ended = False
    start_segment = []
    arrival_segment = []
    route = []
    stations = []
    baseline_length = 0
    env_parameters = {
        "soc0": route_parameters.soc0,
        "soc_min": route_parameters.soc_min,
        "soh": route_parameters.soh,
        "k": route_parameters.k,
        "t": route_parameters.t,
        "n_pass": route_parameters.n_pass
    }
    while not search_ended:
        baseline = shortest_path(start_edge, end_edge)
        direct_route_edges = convert_from_point_to_edges(baseline)
        if numstop == 0:
            baseline_length = calculate_distance(direct_route_edges)
        direct_route = Path(points=baseline)
        feasibility = await direct_route.is_feasible(**env_parameters, vehicle_parameters=vehicle_parameters)
        if feasibility:
            search_ended = True
            route = start_segment + direct_route_edges + arrival_segment
        else:
            numstop += 1
            if numstop % 2 == 1:
                best_station, best_edges = await evaluate_start_to_station(baseline=baseline, start=start_edge,
                                                                           env_parameters=env_parameters, vehicle_parameters=vehicle_parameters)
                if best_station is not None:
                    start_edge = best_station
                    start_segment += best_edges
                    stations.append(best_station)
                else:
                    return [], [], None
            else:
                best_station, best_edges = await evaluate_station_to_end(baseline=baseline, end=end_edge,
                                                                         env_parameters=env_parameters, vehicle_parameters=vehicle_parameters)
                if best_station is not None:
                    end_edge = best_station
                    arrival_segment = best_edges + arrival_segment
                    stations.append(best_station)
                else:
                    return [], [], None
    score = baseline_length / calculate_distance(route)
    route = swap_coordinates(route)
    stations = swap_coordinates(stations)
    return route, stations, score
