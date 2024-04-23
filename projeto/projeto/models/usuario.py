from pydantic import BaseModel
from datetime import datetime

class Usuario(BaseModel):
    id: int
    name: str
    email: str
    password: str
    cpf: str

class UsuarioCreate(BaseModel):
    name: str
    email: str
    password: str
    cpf: str