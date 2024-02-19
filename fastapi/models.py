from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import functions
from datetime import datetime

from database import Base


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    limite: Mapped[int] = mapped_column(nullable=False)
    saldo: Mapped[int] = mapped_column(nullable=False)

    # Establish a one-to-many relationship with the 'transaction' table
    transaction: Mapped[list['Transaction']] = relationship(back_populates='client')

class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    valor: Mapped[int] = mapped_column(nullable=False)
    tipo: Mapped[str] = mapped_column(String(1), nullable=False)
    descricao: Mapped[str] = mapped_column(String(10), nullable=False)
    #With timezone
    #realizada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=functions.now(), nullable=False)
    #Without timezone
    realizada_em: Mapped[datetime] = mapped_column(server_default=functions.now(), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)

    client: Mapped['Client'] = relationship(back_populates='transaction')
