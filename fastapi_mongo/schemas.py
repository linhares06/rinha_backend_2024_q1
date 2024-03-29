from pydantic import BaseModel, Field
from datetime import datetime


class Client(BaseModel):
    id: int
    limite: int
    saldo: int
    transactions: list['TransactionResponseSchema'] = []

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
    total: int = Field(alias='saldo')
    data_extrato: datetime = Field(default_factory=datetime.now)
    limite: int

class StatementResponseSchema(BaseModel):
    saldo: StatementSchema
    ultimas_transacoes: list[TransactionResponseSchema]


                                               