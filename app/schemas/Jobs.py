from datetime import date, datetime
from pydantic import BaseModel
from enum import Enum

class JobCategory(str, Enum):
    IT = 'IT'
    Finance = 'Finance'
    Marketing = 'Marketing'
    UI_UX = 'UI/UX'
    Web_Development = 'Web Development'
    Frontend_Developer = 'Frontend Developer'
    Backend_Developer = 'Backend Developer'
    Full_Stack = 'Full Stack'

class Jobs(BaseModel):
    # jobid: int
    title: str
    jobDescription: str
    minYearsOfExperience: float
    category: JobCategory
    lastDateToRegister: date
    companyName: str
    companyDescription: str
    stipend: str
    active: int = ""
