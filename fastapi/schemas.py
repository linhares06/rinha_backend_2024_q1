from pydantic import BaseModel, Field
from datetime import datetime


class Client(BaseModel):
    id: int
    limite: int
    saldo: int

class TransactionSchema(BaseModel):
    valor: int = Field(gt=0)
    tipo: str = Field(pattern="^(c|d)$") 
    descricao: str = Field(min_length=1, max_length=10)

class TransactionResponseSchema(TransactionSchema):
    realizada_em: datetime

class CreateTransactionResponseSchema(BaseModel):
    limite: int
    saldo: int

class StatementSchema(BaseModel):
    saldo: dict
    ultimas_transacoes: list[TransactionSchema]# 10 ultimas transacoes descrescente por data/hora 
                                               