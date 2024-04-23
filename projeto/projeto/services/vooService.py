from fastapi import HTTPException, status
from models.voo import VooModel
from data.database import Voo
from datetime import datetime, date
import logging
from sqlalchemy import and_

logging.basicConfig(level=logging.INFO)


class VooCrud:
    def __init__(self, db_session):
        self.db_session = db_session

    def cadastrar_voo(self, voo: VooModel):
        voo_decode = voo.model_dump()
        voo_banco = Voo(**voo_decode)
        
        try:
            self.db_session.add(voo_banco)
            self.db_session.commit()
        except Exception as e:
            logging.error(
                "Erro ao registrar novo Aerporto" + str(voo_decode) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar aerporto no banco",
            )

        return VooModel(**voo_decode)

    def listar_voos(self):
        voos = self.db_session.query("voos").all()
        voos_decode = []
        for voo in voos:
            voo_decode = voo.__dict__
            voos_decode.append(voo_decode)

        return voos_decode


    from datetime import datetime

    def listar_voos_data(self, data_voo: str):
        try:
            # Convert string representation of date to datetime object
            data_voo_datetime = datetime.strptime(data_voo, "%Y-%m-%d").date()
            logging.info(data_voo_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de data inválido. Utilize o formato AAAA-MM-DD.",
            )

        voos = self.db_session.query(Voo).filter(Voo.departure_date == data_voo_datetime).all()
        voos_decode = []
        for voo in voos:
            voo_decode = voo.__dict__
            voos_decode.append(voo_decode)

        return voos_decode

    
    from sqlalchemy import and_  # Import for combining query filters

    def get_flights_by_price_and_availability(self,
        available_seats_threshold: int,
        flight_date: str,
        origin_city: str,
        destination_city: str):
        
        filters = [Voo.available_tickets >= available_seats_threshold]  # Initialize empty list of filters

        if flight_date != "Any":
            try:
                flight_date_obj = datetime.strptime(flight_date, "%Y-%m-%d").date()
                filters.append(Voo.departure_date == flight_date_obj)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Formato de data inválido. Utilize o formato AAAA-MM-DD.",
                )

        if origin_city != "Any":
            filters.append(Voo.origin_city == origin_city)

        if destination_city != "Any":
            filters.append(Voo.destination_city == destination_city)

        filtered_flights = (
            self.db_session.query(Voo)
            .filter(and_(*filters))  # Apply all filters using `and_`
            .order_by(Voo.price)  # Order by price ascending
            .all()
        )

        return filtered_flights  # Assuming you can directly return VooModel objects



    def listar_voos_origem(self, origem: str):
        voos = self.db_session.query(Voo).filter(VooModel.origin_city == origem).all()
        voos_decode = []
        for voo in voos:
            voo_decode = voo.__dict__
            voos_decode.append(voo_decode)

        return voos_decode



    def get_voo(self, id_voo: int):
        voo = self.db_session.query(Voo).filter(VooModel.id == id_voo).first()
        if voo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aeroporto não encontrado",
            )

        voo_decode = voo.__dict__
        return voo_decode
