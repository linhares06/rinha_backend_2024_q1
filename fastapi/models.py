from sqlalchemy import Column, Integer

from database import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    limit = Column(Integer)
    opening_balance = Column(Integer)

