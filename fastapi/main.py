from fastapi import FastAPI, Depends, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from db_session import get_db
from schemas import Client as ClientSchema, TransactionSchema, StatementSchema, CreateTransactionResponseSchema
from models import Client, Transaction


app = FastAPI()

@app.post('/clientes/{id}/transacoes', response_model=CreateTransactionResponseSchema | dict)
async def transaction(id: int, transaction: TransactionSchema, response: Response, db: Session = Depends(get_db)):
    #crédito adiciona, débito remove do saldo
    #Uma transação de débito nunca pode deixar o saldo do cliente menor que seu limite disponível.
    #Exemplo: um cliente com limite de 1000 nunca deverá ter o saldo menor que -1000. Caso seja menor que -1000, rollback e retornar 422
    #Se o id da URL for inexistente (exemplo: 6), a API deve retornar HTTP Status Code 404.
    
    try:
        client_model = db.query(Client).filter_by(id=id).one()
        transaction_model = Transaction(**transaction.model_dump())
        
        if transaction_model.tipo == 'd':
            saldo = client_model.saldo - transaction_model.valor
            if saldo + client_model.limite < 0:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'limite': 'Ta querendo gastar mais do que tem, champz'}   
        else:
            saldo = client_model.saldo + transaction_model.valor

        client_model.saldo = saldo
        transaction_model.client_id = client_model.id

        db.add(client_model)
        db.add(transaction_model)
        db.commit()
        db.refresh(client_model)

    except NoResultFound:
        response.status_code = status.HTTP_404_NOT_FOUND
    except Exception as e:
        db.rollback()
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'error': str(e)}

    return client_model

@app.get('/clientes/{id}/extrato', response_model=StatementSchema)
async def transaction():
    return ''

# Endpoints de teste
@app.get('/clientes', response_model=list[ClientSchema])
async def test_get_all_Client(db: Session = Depends(get_db)):
    users = db.query(Client).all()

    return users
