from datetime import date
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from enum import Enum as PyEnum


class StatusEnum(str, PyEnum):
    APPLIED = "APPLIED"
    UNDER_CONSIDERATION = "UNDER_CONSIDERATION"
    REJECTED = "REJECTED"
    HIRED = "HIRED"

class ApplicationSchema(BaseModel):
    firstName : str = " "
    middleName : str = " "
    lastName : str = " "
    email : str = " "
    phone : str = " "
    resumeLink : str = " "
    minYearsOfExperience : str  = " "
    status: StatusEnum


