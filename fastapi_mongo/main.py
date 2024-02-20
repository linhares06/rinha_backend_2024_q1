from fastapi import FastAPI, Response, status
from datetime import datetime

from database import Database
from schemas import Client as ClientSchema, TransactionSchema, CreateTransactionResponseSchema, StatementResponseSchema

app = FastAPI()

db = Database()

@app.post('/clientes/{id}/transacoes', response_model=CreateTransactionResponseSchema | dict)
async def transaction(id: int, transaction: TransactionSchema, response: Response):
    #crédito adiciona, débito remove do saldo
    #Uma transação de débito nunca pode deixar o saldo do cliente menor que seu limite disponível.
    #Exemplo: um cliente com limite de 1000 nunca deverá ter o saldo menor que -1000. Caso seja menor que -1000, rollback e retornar 422
    #Se o id da URL for inexistente (exemplo: 6), a API deve retornar HTTP Status Code 404.

    try:
        client = db.clients_collection.find_one({'id': id}, {'_id': 0, 'transactions': 0})
        
        if not client:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'error': 'Id inexistente'}
        
        client_schema = ClientSchema.model_validate(client)
        
        if transaction.tipo == 'd':
            saldo = client_schema.saldo - transaction.valor
            if saldo + client_schema.limite < 0:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'limite': 'Ta querendo gastar mais do que tem, champz'}   
        else:
            saldo = client_schema.saldo + transaction.valor

        client_schema.saldo = saldo

        transaction_dict = transaction.model_dump()
        transaction_dict['realizada_em'] = datetime.now()

        result = db.clients_collection.update_one(
            {'id': id},
            {'$set': {'saldo': saldo}, '$push': {'transactions': transaction_dict}},
            upsert=True
        )

        if result.modified_count == 0:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {'error': 'error'}
            
    except Exception as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'error': str(e)}

    return client_schema

@app.get('/clientes/{id}/extrato', response_model_by_alias=False, response_model=StatementResponseSchema | dict)
async def statement(id: int, response: Response):

    try:
        client = db.clients_collection.find_one({'id': id}, {'_id': 0, 'id': 0, 'transactions': 0})

        if not client:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'error': 'Id inexistente'}
        
        pipeline = [
            {'$match': {'id': id}},
            {'$project': {'_id': 0, 'id': 0, 'saldo': 0, 'limite': 0}},
            {'$unwind': '$transactions'},
            {'$sort': {'transactions.realizada_em': -1}},
            {'$limit': 10},
        ]

        last_transactions = [doc['transactions'] for doc in list(db.clients_collection.aggregate(pipeline))]
        
        statement = StatementResponseSchema(saldo=client, ultimas_transacoes=last_transactions)

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'error': str(e)}

    return statement


# Endpoints de teste
@app.get('/clientes', response_model=list[ClientSchema])
async def test_get_all_Client():
    return db.clients_collection.find()
    