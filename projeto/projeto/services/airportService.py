from fastapi import HTTPException, status
from models.airport import AirportModel
from data.database import Airport
from models.voo import VooModel
from data.database import Voo
from services.vooService import VooCrud
import logging

logging.basicConfig(level=logging.INFO)



class AirportCrud:
    def __init__(self, db_session):
        self.db_session = db_session

    def cadastrar_airport(self, airport: AirportModel):
        airport_decode = airport.model_dump()
        airport_banco = Airport(**airport_decode)
        
        try:
            self.db_session.add(airport_banco)
            self.db_session.commit()
        except Exception as e:
            logging.error(
                "Erro ao registrar novo Aerporto" + str(airport_decode) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar aerporto no banco",
            )

        return AirportModel(**airport_decode)

    def listar_aerportos(self):
        airports = self.db_session.query(Airport).all()
        airports_decode = []
        for airport in airports:
            airport_decode = airport.__dict__
            airports_decode.append(airport_decode)

        return airports_decode
    
    def listar_aerportos_destino(self, origem: str):
        # Retrieve all destination airports
        aeroportos_destino = (
            self.db_session.query(Airport)
            .join(Voo, Airport.id == Voo.destination_id)
            .distinct()
        )

        # Filter out airports with no flights from the origin
        aeroportos_destino_filtrados = []
        for airport in aeroportos_destino:
            voo_count = (
                self.db_session.query(Voo)
                .filter(Voo.origin_city == origem)
                .count()
            )
            if voo_count > 0:
                aeroportos_destino_filtrados.append(airport)

        # Convert to list of dictionaries
        aeroportos_decode = []
        for airport in aeroportos_destino_filtrados:
            airport_decode = airport.__dict__
            aeroportos_decode.append(airport_decode)

        return aeroportos_decode



    def get_aerporto(self, id_airport: int):
        airport = self.db_session.query(Airport).filter(Airport.id == id_airport).first()
        if airport is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aeroporto não encontrado",
            )

        airport_decode = airport.__dict__
        return airport_decode
