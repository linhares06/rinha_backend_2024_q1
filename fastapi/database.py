import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

db_driver = os.getenv('DB_DRIVER')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
postgres_db = os.getenv('POSTGRES_DB')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')

DATABASE_URL = f'{db_driver}://{postgres_user}:{postgres_password}@{db_host}:{db_port}/{postgres_db}'


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()