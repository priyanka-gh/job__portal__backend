from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from app.db.session import Base
from app.db.session import engine


class User(Base):
    __tablename__ = "User"
    userid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(30), unique = True)
    password = Column(String(15))
    role = Column(Integer())

    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)
