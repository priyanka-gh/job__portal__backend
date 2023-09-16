from sqlalchemy.schema import Column
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from app.db.session import Base
from app.db.models import Users
from app.db.session import engine

class UserProfile(Base):
    __tablename__ = "UserProfile"
    profileid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(Integer, ForeignKey(Users.User.userid))
    firstName = Column(String(15))
    middleName = Column(String(15))
    lastName = Column(String(15))
    email = Column(String(30), unique = True)
    phone = Column(String(10))
    roleTitle = Column(String(255))


    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)