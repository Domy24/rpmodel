from pydantic import BaseModel


class Route(BaseModel):
    start: str
    end: str


class ResponseRoute(BaseModel):
    segments: list
