from pydantic import BaseModel
from geopy.distance import geodesic
from .utils import driverMaxSpeed, driverMaxAcc
class Path(BaseModel):
    start: str
    end: str
    points: list[dict]

    def is_feasible(self, soc0, soc_min, soh, k, energyUsable) -> bool:
        n_edges = len(self.points) - 1
        feasible = True
        counter = 1
        energyIntegral = 0
        energyAvailable = energyUsable * (soc0 - soc_min * soh * k)/0.8
        actualSpeed = 0
        flag = True
        while counter < n_edges and flag:
            lengthRun = 0
            length = geodesic(self.points[counter]["point"], self.points[counter-1]["point"]).meters
            while lengthRun < length:
                lengthRun = lengthRun + actualSpeed
                if lengthRun > length:
                    counter+=1
                    if counter > n_edges:
                        break
                nextSpeed = min(self.points[counter]["speed"], driverMaxSpeed(k))
                acc = nextSpeed - actualSpeed
                if acc <= -4.5:
                    acc = 4.5
                if acc >= driverMaxAcc(k):
                    acc = driverMaxAcc(k)






