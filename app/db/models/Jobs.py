from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, Date, DateTime, Boolean
from sqlalchemy import Enum
from app.db.session import Base
from app.db.models import Users
from app.db.session import engine


class Jobs(Base):
    __tablename__ = "Jobs"
    jobid = Column(Integer, primary_key = True, index = True)
    title = Column(String(255))
    jobDescription = Column(String(255))
    minYearsOfExperience = Column(Integer)
    category = Column(Enum('IT','Finance','Marketing','UI/UX','Web Development','Frontend Developer','Backend Developer','Full Stack'))
    lastDateToRegister = Column(Date)
    companyName = Column(String(255))
    companyDescription = Column(String(255))
    postedBy = Column(String(255))
    postedAt = Column(DateTime)
    updatedAt = Column(DateTime)
    active = Column(Integer)
    stipend = Column(String(255))

    
    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)