from pydantic import BaseModel

class AirportModel(BaseModel):
    id: int
    name: str
    city: str
