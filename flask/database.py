import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    return SQLAlchemy(app)

Base = declarative_base()