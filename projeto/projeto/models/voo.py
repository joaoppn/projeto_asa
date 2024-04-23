from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone, date


class VooModel(BaseModel):
    id: int
    origin_id : int
    destination_id: int
    origin_city: str
    destination_city: str
    departure_date: date
    price: int
    available_tickets: int


