from fastapi import FastAPI
from schemas import Client as ClientSchema
from models import Client as ClientModel

from database import DBSession


app = FastAPI()

@app.post('/clientes/{id}/transacoes')
async def transaction():
    return ''

@app.get('/clientes/{id}/extrato')
async def transaction():
    return ''


@app.get('/', response_model=list[ClientSchema])
async def test_get_all_Client():
    session = DBSession()
    users = session.query(ClientModel).all()
    session.close()

    return users
