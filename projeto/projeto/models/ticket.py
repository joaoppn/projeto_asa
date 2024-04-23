from pydantic import BaseModel
from models.voo import VooModel
from models.usuario import Usuario
from datetime import datetime, timedelta, timezone

class TicketModel(BaseModel):
    id: int
    flight_id: int
    usuario_id: int
    e_ticket: str

    