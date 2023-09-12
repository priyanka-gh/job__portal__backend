from pydantic import BaseModel

class UserProfile(BaseModel):
    firstName: str
    middleName: str
    lastName: str
    # email: str
    phone: str
    roleTitle: str
