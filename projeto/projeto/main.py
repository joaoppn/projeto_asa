from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from models.usuario import Usuario as UsuarioModel 
from models.voo import VooModel
from models.ticket import TicketModel
from models.airport import AirportModel
from data.database import session, Usuario
from services.usuarioService import UsuarioCrud
from services.vooService import VooCrud
from services.ticketService import ReservaCrud
from services.airportService import AirportCrud
from pydantic import BaseModel
import logging
from datetime import datetime, date
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    email: str
    password: str

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
usuario_crud = UsuarioCrud(db_session=session)
voo_crud = VooCrud(db_session=session)
reserva_crud = ReservaCrud(db_session=session)
airport_crud = AirportCrud(db_session=session)

#Login

# def get_current_user_id(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, ACCESS_TOKEN_EXPIRE_MINUTES, algorithms=["HS256"])
#         email: str = payload.get("sub")
#         logging.info(f"Email = {email}")
#         if email is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Não foi possível validar as credenciais.",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         user = session.query(Usuario).filter(Usuario.email == email).first()  # Assuming you have this function
#         logging.info(f"user = {user}")
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Usuário não encontrado."
#             )
#         return user.id
#     except JWTError as e:  # Catch potential decoding or authentication errors
#         raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Não foi possível validar as credenciais.",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )


@app.post("/token", tags=["Token"])
async def login_for_access_token(form_data: TokenData):
    return usuario_crud.login_for_access_token(form_data)

@app.post("/usuario/cadastro", response_model=UsuarioModel, tags=["Usuário"])
async def cadastrar_usuario(usuario: UsuarioModel):
    return usuario_crud.cadastrar_usuario(usuario)

@app.get("/usuario/{id_usuario}", response_model=UsuarioModel, tags=["Usuário"])
async def get_usuario(id_usuario: int):
    return usuario_crud.get_usuario(id_usuario)

#Voo - Cadastro | Retorno por ID | Retorno por Data

@app.post("/voo/cadastro", response_model=VooModel, tags=["Voo"])
async def cadastrar_voo(voo: VooModel):
    return voo_crud.cadastrar_voo(voo)

@app.get("/voo/{id_voo}", response_model=VooModel, tags=["Voo"])
async def get_voo(id_voo: int):
    return voo_crud.get_voo(id_voo)

@app.get("/voo/data/{data}",  response_model=list[VooModel], tags=["Voo"])
async def listar_voos_data(data: str):
    return voo_crud.listar_voos_data(data)

@app.get("/voo/busca/{seats}/{date}/{origin}/{destination}", response_model=list[VooModel], tags=["Voo"])
async def get_flights_by_price_and_availability(seats: str, date: str="Any", origin:str="Any", destination:str="Any"):
    return voo_crud.get_flights_by_price_and_availability(seats, date, origin, destination)

#Aerporto - Cadastro | Aerportos Destino - Origem |Listar todos

@app.post("/aeroporto/cadastro", response_model=AirportModel, tags=["Airport"])
async def cadastrar_aeroporto(aerporto: AirportModel):
    return airport_crud.cadastrar_airport(aerporto)

@app.get("/aeroporto/origem/{origem}", response_model=list[AirportModel], tags = ["Airport"])
async def listar_aerportos_destino(origem: str):
    return airport_crud.listar_aerportos_destino(origem)

@app.get("/aeroporto/list", response_model=list[AirportModel], tags = ["Airport"])
async def listar_aerportos():
    return airport_crud.listar_aerportos()


#Tickets - Comprar(Cadastrar) | Localizar 


@app.post("/ticket/{voo_id}/{ticket_id}", response_model=TicketModel, tags=["Reserva"])
async def comprar_passagem(voo_id: int, ticket_id: int, user_id: int= 0) :
    return reserva_crud.comprar_passagem(voo_id, ticket_id, user_id)