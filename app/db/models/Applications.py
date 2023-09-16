from sqlalchemy.schema import Column
from sqlalchemy import DateTime, ForeignKey, BLOB, String, Integer, Text, Double
from app.db.session import Base
from app.db.models import Users
from app.db.models import Jobs
from sqlalchemy import Enum
from app.db.session import engine

class Application(Base):
    __tablename__ = "Applications"
    applicationid = Column(Integer, primary_key = True, index = True)
    userId = Column(Integer, ForeignKey(Users.User.userid))
    jobId = Column(Integer, ForeignKey(Jobs.Jobs.jobid))
    firstName = Column(String(15))
    middleName = Column(String(15))
    lastName = Column(String(15))
    email = Column(String(30))
    phone = Column(String(10))
    resumeLink = Column(String(255))
    minYearsOfExperience = Column(String(255))
    appliedAt = Column(DateTime)
    status = Column(Enum('APPLIED','UNDER_CONSIDERATION','REJECTED','HIRED'))


    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)