from fastapi import Request, Form, APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from app.utils.util import verify_token
from app.schemas.Users import UserSchema
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.auth_service import get_token, signup

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: str

@router.post("/signup")
def signup_service(user : UserSchema):
    return signup(user)

@router.post("/token")
async def login(
    password: str = Form(...),
    email: str = Form(...)
):
    db = SessionLocal()
    return get_token(email, password, db)

# @router.post("/logout")
# def logout(token_data: dict = Depends(verify_token)):
#     return {"message": "Logout successful."}