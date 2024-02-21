from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound

from database import get_db
from models import Client as ClientModel, Transaction as TransactionModel
from schemas import Client as ClientSchema, StatementResponseSchema, TransactionSchema, CreateTransactionResponseSchema

app = Flask(__name__)
api = Api(app)

db: SQLAlchemy = get_db(app)


class Clients(Resource):
    def get(self):
        clients = db.session.query(ClientModel).all()
        clients_schema = [ClientSchema.model_validate(client.__dict__).model_dump() for client in clients]

        return jsonify(clients_schema)
    
    
class Statement(Resource):
    def get(self, id):
        try:
            #Descobrir como pegar client_model com as 10 ultimas transactions em uma query só
            client_model = db.session.query(ClientModel).filter_by(id=id).one()

            transaction_models = db.session.query(TransactionModel).filter_by(client_id=id)\
                        .order_by(desc(TransactionModel.realizada_em))\
                        .limit(10)\
                        .all()

            statement = StatementResponseSchema(saldo=client_model, ultimas_transacoes=transaction_models)

        except NoResultFound:
            return {'error': 'Id inexistente'}, 404 
        except Exception as e:
            return {'error': str(e)}, 422

        return jsonify(statement.model_dump())

class Transaction(Resource):
    def post(self, id):
        try:        
            request_data = request.get_json()
            valor = request_data.get('valor')
            tipo = request_data.get('tipo')
            descricao = request_data.get('descricao')

            transaction = TransactionSchema(valor=valor, tipo=tipo, descricao=descricao)

            client_model = db.session.query(ClientModel).filter_by(id=id).one()
            transaction_model = TransactionModel(**transaction.model_dump())
            
            if transaction_model.tipo == 'd':
                saldo = client_model.saldo - transaction_model.valor
                if saldo + client_model.limite < 0:
                    return {'limite': 'Ta querendo gastar mais do que tem, champz'}, 422
            else:
                saldo = client_model.saldo + transaction_model.valor

            client_model.saldo = saldo
            transaction_model.client_id = client_model.id

            db.session.add(client_model)
            db.session.add(transaction_model)
            db.session.commit()
            db.session.refresh(client_model)

        except NoResultFound:
            return {'error': 'Id inexistente'}, 404
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 422

        return jsonify(CreateTransactionResponseSchema.model_validate(client_model.__dict__).model_dump())

api.add_resource(Clients, '/')
api.add_resource(Transaction, '/clientes/<int:id>/transacoes')
api.add_resource(Statement, '/clientes/<int:id>/extrato')

if __name__ == '__main__':
    app.run(debug=True)