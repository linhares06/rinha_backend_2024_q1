from fastapi import FastAPI, Depends
from schemas import Client as ClientSchema
from models import Client as ClientModel
from sqlalchemy.orm import Session

from db_session import get_db


app = FastAPI()

@app.post('/clientes/{id}/transacoes')
async def transaction():
    return ''

@app.get('/clientes/{id}/extrato')
async def transaction():
    return ''


@app.get('/clientes', response_model=list[ClientSchema])
async def test_get_all_Client(db: Session = Depends(get_db)):
    users = db.query(ClientModel).all()

    return users
