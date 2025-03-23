from typing import Optional

from pydantic import BaseModel, Field, validator, root_validator


class Route(BaseModel):
    start: str
    end: str
    id: Optional[int]

class RouteSegments(BaseModel):
    segments: Optional[list] = []
    stations: Optional[list] = []
    detail: Optional[str] = None
    score: Optional[float] = None

class RouteUserDetail(BaseModel):
    start: str
    end: str
    route: RouteSegments

class RouteUserList(BaseModel):
    routes: Optional[list[Route]] = []


class VehicleParameters(BaseModel):
    model: str
    weight_kg: float
    cd_area: float
    velocity_mps: float
    motor_efficiency: float
    front_area: float
    mu_r: float
    vtype: str
    energy_usable: float

    @validator("vtype")
    def vtype_valid(cls, value):
        if value not in ["Small SUV", "City Car", "Gran Turismo Sedan"]:
            raise ValueError("Tipo non supportato.")
        return value

    @validator("weight_kg")
    def weight_kg_valid(cls, value):
        if not value > 0:
            raise ValueError("Il peso del veicolo deve essere positivo")
        return value

    @validator('cd_area')
    def cd_area_positive(cls, value):
        if value <= 0:
            raise ValueError("L'area di resistenza aerodinamica deve essere un valore positivo")
        return value

    @validator('velocity_mps')
    def velocity_positive(cls, value):
        if value <= 0:
            raise ValueError("La velocità deve essere un valore positivo")
        return value

    @validator('motor_efficiency')
    def motor_efficiency_valid(cls, value):
        if not (0 <= value <= 1):
            raise ValueError("L'efficienza del motore deve essere un valore compreso tra 0 e 1")
        return value

    @validator('front_area')
    def front_area_positive(cls, value):
        if value <= 0:
            raise ValueError("L'area frontale deve essere un valore positivo")
        return value

    @validator('mu_r')
    def mu_r_positive(cls, value):
        if value < 0:
            raise ValueError("Il coefficiente di resistenza del rotolamento non può essere negativo")
        return value


class EnvParameters(BaseModel):
    soc0: float
    soc_min: float
    soh: float
    k: float
    t: float
    n_pass: int

    @validator("soc0")
    def soc0_valid(cls, value, values):
        soc_min = values.get("soc_min")
        if soc_min is not None and value <= soc_min:
            raise ValueError("SoC0 deve essere più grande di SoCmin.")
        if value > 100 or value < 0:
            raise ValueError("SoC0 deve essere compreso tra 0% e 100%.")
        return value/100

    @validator("soc_min")
    def soc_min_valid(cls, value):
        if not 0 < value <= 100:
            raise ValueError("SoCmin deve essere compreso tra 0 e 100%.")
        return value/100

    @validator("soh")
    def soh_valid(cls, value):
        if not 0 < value < 100:
            raise ValueError("SoH deve essere compreso tra 0 e 100%.")
        return value/100

    @validator("k")
    def k_valid(cls, value):
        if value not in [0.6, 0.5, 0.9]:
            raise ValueError("K può essere: 0.5, 0.6, 0.9.")
        return value

    @validator("t")
    def t_valid(cls, value):
        if not -50 < value < 50:
            raise ValueError("Inserire una temperatura compresa tra -50 e 50.")
        return value

    @validator("n_pass")
    def n_pass_valid(cls, value):
        if not 0 <= value < 4:
            raise ValueError("Il numero di passeggeri deve essere compreso tra 0 e 4.")
        return value


class RouteParameters(BaseModel):
    start: str
    end: str
    route_parameters: EnvParameters
    vehicle_parameters: VehicleParameters

class RouteRequest(BaseModel):
    parameters: RouteParameters

