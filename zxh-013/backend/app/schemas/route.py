from pydantic import BaseModel, Field


class RoutePoint(BaseModel):
    lat: float
    lng: float


class RouteRequest(BaseModel):
    start_lat: float = Field(ge=-90, le=90)
    start_lng: float = Field(ge=-180, le=180)
    end_lat: float = Field(ge=-90, le=90)
    end_lng: float = Field(ge=-180, le=180)


class RouteResponse(BaseModel):
    direct_path: list[RoutePoint]
    optimized_path: list[RoutePoint]
    avoided_markers: int
