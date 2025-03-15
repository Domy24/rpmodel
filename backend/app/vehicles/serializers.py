from pydantic import BaseModel


class Vehicle(BaseModel):
    model: str
    weight_kg: float
    cd_area: float
    velocity_mps: float
    motor_efficiency: float
    front_area: float
    mu_r: float
    vtype: str
    energy_usable: float


class VehicleList(BaseModel):
    vehicles: list[Vehicle]
