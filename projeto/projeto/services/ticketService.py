from fastapi import HTTPException, status
from models.ticket import TicketModel
from models.voo import VooModel
from data.database import Ticket, Voo
from sqlalchemy.orm import Session
import logging
import math

from amqp.publisher import Publisher # type: ignore

logging.basicConfig(level=logging.INFO)

import uuid
def generate_uuid():
    return uuid.uuid4()


class ReservaCrud:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def comprar_passagem(self,voo_id: int, ticket_id: int, user_id: int):
        # 1. Retrieve Flight and Validate Available Tickets
        voo = self.db_session.query(Voo).filter(Voo.id == voo_id).first()
        if not voo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voo não encontrado."
            )

        if voo.available_tickets <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não há passagens disponíveis para este voo."
            )

        # 2. Generate Ticket
          # We'll define this helper function below
        novo_ticket = TicketModel(
            id = ticket_id,
            flight_id=voo_id,
            usuario_id=user_id,  # Get passenger ID from authenticated user
            e_ticket= str(ticket_id) + "-" + str(voo_id) + "-" + str(user_id))
        
        novo_e_ticket = self._gerar_e_ticket(novo_ticket)

        # 3. Update Available Tickets on Flight
        with self.db_session as session:
            voo.available_tickets -= 1  # Adiciona o ticket na sessão também
            session.commit()

        return novo_e_ticket


    def _gerar_e_ticket(self, ticket: TicketModel):
        ticket_decode = ticket.model_dump()
        ticket_banco = Ticket(**ticket_decode)

        try:
            self.db_session.add(ticket_banco)
            self.db_session.commit()

        except Exception as e:
            logging.error(
                "Erro ao registrar novo Ticket no banco - services/ticketservice.py - cadastrar_ticket() - " + str(ticket_decode) + str(e)
            )
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cadastrar Ticket no banco",
            )
        
        return TicketModel(**ticket_decode)