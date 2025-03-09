from typing import Optional

from pydantic import BaseModel


class Route(BaseModel):
    start: str
    end: str


class RouteSegments(BaseModel):
    segments: list
    stations: Optional[list] = []


class RouteList(BaseModel):
    routes: list[tuple]