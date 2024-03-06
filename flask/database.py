import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import declarative_base

db_driver = os.getenv('DB_DRIVER')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
postgres_db = os.getenv('POSTGRES_DB')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')

DATABASE_URL = f'{db_driver}://{postgres_user}:{postgres_password}@{db_host}:{db_port}/{postgres_db}'

def get_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    return SQLAlchemy(app)

Base = declarative_base()