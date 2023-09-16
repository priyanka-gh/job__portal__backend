from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine("mysql+mysqlconnector://freedb_priyanka:xPwg%jZgehU*2Cv@sql.freedb.tech:3306/freedb_Job_portal", pool_pre_ping=False)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()