import pydantic

class Address(pydantic.BaseModel):
    name: str
    latitude: float
    longitude: float

class LatLong(pydantic.BaseModel):
    min_latitude : float
    max_latitude : float
    min_longitude : float
    max_longitude : float