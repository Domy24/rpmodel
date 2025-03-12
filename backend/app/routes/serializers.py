from typing import Optional

from pydantic import BaseModel


class Route(BaseModel):
    start: str
    end: str


class RouteSegments(BaseModel):
    segments: Optional[list] = []
    stations: Optional[list] = []
    detail: Optional[str] = None


class RouteList(BaseModel):
    routes: list[tuple]