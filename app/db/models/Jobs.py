from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, Date, DateTime, Boolean
from sqlalchemy import Enum
from app.db.session import Base
from app.db.models import Users
from app.db.session import engine


class Jobs(Base):
    __tablename__ = "Jobs"
    jobid = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    jobDescription = Column(String)
    minYearsOfExperience = Column(Integer)
    category = Column(Enum('IT','Finance','Marketing','UI/UX','Web Development','Frontend Developer','Backend Developer','Full Stack'))
    lastDateToRegister = Column(Date)
    companyName = Column(String)
    companyDescription = Column(String)
    postedBy = Column(String)
    postedAt = Column(DateTime)
    updatedAt = Column(DateTime)
    active = Column(Integer)
    stipend = Column(String)

    
    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)