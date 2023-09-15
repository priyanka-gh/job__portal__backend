from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException, status, Depends
import json
import os
from dotenv import load_dotenv
from app.db.models.Users import User
from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from app.db.session import Base
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData
from sqlalchemy.orm.exc import NoResultFound
from fastapi.exceptions import HTTPException as JWTError
from fastapi import Depends, HTTPException, status
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials
from passlib.context import CryptContext
from fastapi import UploadFile
import tempfile

SECRET_KEY = "fd68bbcc397ff21d9073b18ef8d3ba6df9dc22fa68c8a827dfbeef7fc7af7f50"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")
crypt_context = CryptContext(schemes = ["sha256_crypt", "md5_crypt"])


def create_access_token(data: dict, expires_delta: timedelta):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        return e

def get_user(email: str, db: Session):
    user2 = db.query(User).all()
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    except Exception as e:
        return None  


def get_password_hash(password):
    return crypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


def authenticate(email, password, db):
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.email == email).first()

        if user and verify_password(password, user.password):
            return True
        else:
            return False

    except Exception as e:
        raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
    finally:
        db.close()


def exists_with_filters(db: Session, table_class, field_name, field_value) -> bool:
    table = table_class
    try:
        query = db.query(table)
        query = query.filter(getattr(table, field_name) == field_value)
        query.one()
        return True
    except NoResultFound:

        return False
   

def get_user_required_field(
    token: str = Depends(oauth2_scheme),
    required_claim: Optional[str] = "email"
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        claim_value = payload.get(required_claim)
        if claim_value is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"{required_claim.capitalize()} not found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return claim_value
    except Exception as e:
        return e


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

#  0 : recruiter 1 : jobseeker
def check_user_role(token: dict = Depends(verify_token)):
    user_role = token.get("role")  # Assuming "role" is included in the token
    if user_role != 0:  # Adjust the condition based on your role values
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. User role is not allowed.",
        )
    return True


cred = credentials.Certificate("app/services/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'wide-cargo-388709.appspot.com'})


def upload_resume(email: str, resume_file: UploadFile) -> str:
    try:
        print("gigi ",resume_file)
        # Create a temporary file to store the uploaded resume content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(resume_file.file.read())
        
        resume_path = temp_file.name

        bucket = storage.bucket()
        blob = bucket.blob(f"resumes/{email}-{datetime.now().timestamp()}.pdf")
        blob.upload_from_filename(resume_path)
        blob.make_public()
        print("Public URL:", blob.public_url)

        temp_file.close()

        return blob.public_url
    except Exception as e:
        print("Error:", str(e))
        return ""