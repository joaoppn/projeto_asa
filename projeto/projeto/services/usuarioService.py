from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt import create_access_token
from models.usuario import Usuario as UsuarioModel
from data.database import session, Usuario
from datetime import timedelta, datetime
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class TokenData(BaseModel):
    email: str
    password: str

class UsuarioCrud:
    def __init__(self, db_session):
        self.db_session = db_session

    def login_for_access_token(self, form_data: TokenData):
        user = self.db_session.query(Usuario).filter(Usuario.email == form_data.email).first()
        if user is None or not pwd_context.verify(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username ou password estão incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}



    def cadastrar_usuario(self, usuario: UsuarioModel):
        usuario_decode = usuario.model_dump()

        usuario_decode["password"] = pwd_context.hash(usuario_decode["password"])
        usuario_banco = Usuario(**usuario_decode)
        
        try:
            self.db_session.add(usuario_banco)
            self.db_session.commit()
        except Exception as e:
            logging.error(
                "Erro ao registrar novo usuário no banco - controllers/main.py - cadastrar_usuario() " + str(usuario_decode) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar usuário no banco",
            )

        return UsuarioModel(**usuario_decode)

    def listar_usuarios(self):
        usuarios = self.db_session.query(Usuario).all()
        usuarios_decode = []
        for usuario in usuarios:
            usuario_decode = usuario.__dict__
            usuarios_decode.append(usuario_decode)

        return usuarios_decode

    def get_usuario(self, id_usuario: int):
        usuario = self.db_session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        usuario_decode = usuario.__dict__
        return usuario_decode

   

    def update_usuario(self, id_usuario: int, usuario_update: UsuarioModel):
        try:
            usuario_banco = self.db_session.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
            if not usuario_banco:
                raise HTTPException(
                    status_code=404,
                    detail="Usuário não encontrado",
                )

            usuario_banco.name = usuario_update.name
            usuario_banco.email = usuario_update.email
            usuario_banco.password = pwd_context.hash(usuario_update.password)
            usuario_banco.cpf = usuario_update.cpf

            self.db_session.commit()

            return usuario_banco
    
        except Exception as e:
            logging.error(
                "Erro ao atualizar usuário no banco - controllers/main.py - update_usuario() " + str(usuario_update) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar usuário no banco",
            )
