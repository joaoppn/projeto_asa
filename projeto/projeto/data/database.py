from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database
from logger import logger
from sqlalchemy.engine import URL
import os




SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(engine.url):
    logger.info("Criando base de dados")
    create_database(engine.url)
else:
    pass

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    cpf = Column(String, unique=True)

class Sessao(Base):
    __tablename__ = "sessoes"
    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String, unique=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuarios = relationship("Usuario", back_populates="sessoes")

class Airport(Base):
    __tablename__ = "aeroportos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    city = Column(String)

class Voo(Base):
    __tablename__ = "voos"
    id = Column(Integer, primary_key=True, index=True)
    origin_city= Column(String)
    destination_city= Column(String)
    origin_id= Column(Integer, ForeignKey("aeroportos.id"))
    destination_id = Column(Integer, ForeignKey("aeroportos.id"))
    departure_date = Column(Date)
    price = Column(Integer)
    available_tickets= Column(Integer)


class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("voos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    e_ticket = Column(String, unique=True)

Usuario.sessoes = relationship("Sessao", back_populates="usuarios")

# Create all tables in the engine
Base.metadata.create_all(engine)
