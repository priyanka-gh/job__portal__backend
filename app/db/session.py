from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DB_URL = os.environ.get("DB_URL")
engine = create_engine(
    "sqlite:///./sql_app.db",
    connect_args = {"check_same_thread":False},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()