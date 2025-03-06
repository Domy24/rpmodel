from random import random
from typing import Optional

from pydantic import BaseModel
from geopy.distance import geodesic
from .utils import driverMaxSpeed, driverMaxAcc, get_vehicle_parameters, compute_required_power


class Path(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None
    points: list[dict]

    async def is_feasible(self, soc0, soc_min, soh, k, energyUsable, vehicle="ciao") -> bool:
        # energyUsable in kWh
        # parameters = await get_vehicle_parameters(vehicle)
        parameters = {
            "weight_kg": 1500.0,
            "cd_area": 0.32,
            "eta": 0.85,
            "front_area": 2.2,
            "mu_r": 0.01,
        }
        n_edges = len(self.points) - 1
        feasible = True
        counter = 1
        energyIntegral = 0
        energyAvailable = energyUsable * (soc0 - soc_min * soh * k) / 0.8 * 3.6e6
        print("Energy Available: ", energyAvailable)
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
