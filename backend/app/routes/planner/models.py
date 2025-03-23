from random import random
from typing import Optional

from pydantic import BaseModel
from geopy.distance import geodesic
from .utils import driverMaxSpeed, driverMaxAcc, get_vehicle_parameters, compute_required_power, calculate_distance, \
    convert_from_point_to_edges, max_distance
from ..serializers import VehicleParameters


class Path(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None
    points: list[dict]

    async def is_feasible(self, t, n_pass, soc0, soc_min, soh, k, vehicle_parameters: VehicleParameters) -> bool:
        # energyUsable in kWh
        # parameters = await get_vehicle_parameters(vehicle)
        parameters = {
            "types": vehicle_parameters.vtype,
            "weight_kg": vehicle_parameters.weight_kg + n_pass * 85,
            "cd_area": vehicle_parameters.cd_area,
            "eta": vehicle_parameters.motor_efficiency,
            "front_area": vehicle_parameters.front_area,
            "mu_r": vehicle_parameters.mu_r,
            "t": t,
            "n_pass": n_pass
        }
        n_edges = len(self.points) - 1
        feasible = True
        counter = 1
        energyIntegral = 0
        energyAvailable = vehicle_parameters.energy_usable * ((soc0 - soc_min) * soh * k) / 0.8 * 3.6e6
        actualSpeed = 0
        flag = True
        while counter < n_edges and flag:
            lengthRun = 0
            length = geodesic(self.points[counter]["point"], self.points[counter - 1]["point"]).meters
            while lengthRun < length:
                lengthRun = lengthRun + actualSpeed
                if lengthRun > length:
                    counter += 1
                    if counter > n_edges:
                        break
                nextSpeed = min(self.points[counter]["speed"], driverMaxSpeed(k))
                acc = nextSpeed - actualSpeed
                if acc <= -4.5:
                    acc = -4.5
                if acc >= driverMaxAcc(k):
                    acc = driverMaxAcc(k)
                acc += random()
                p_batt = compute_required_power(**parameters, speed=actualSpeed)
                energyIntegral += p_batt
                actualSpeed += acc
                if energyIntegral > energyAvailable:
                    flag = False
                    feasible = False
                    break
        return feasible
