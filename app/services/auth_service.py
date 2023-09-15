from fastapi import HTTPException, status
from app.schemas.Users import UserSchema
from app.db.models.Users import User
from app.db.session import SessionLocal
from app.utils.util import exists_with_filters
from app.utils.util import verify_password, create_access_token, get_user, authenticate, get_password_hash
from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 120


def signup(newUser: UserSchema):
    db = SessionLocal()
    try:
        if exists_with_filters(db, User, "email", newUser.email):
            raise HTTPException(status_code=400, detail="Email already registered")
    except HTTPException as e:
        raise

    try:
        user = User(email = newUser.email,  password = get_password_hash(newUser.password), role = newUser.role)
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return {
            "email" : user.email,
            "userid" : user.userid,
            "role" : user.role
        }

    except Exception as e:
        raise HTTPException(
                status_code=400, detail=str(e)
            )

def get_token(email: str, password: str, db):
    if authenticate(email, password, db):
        user_data = get_user(email, db)
        try:
            access_token = create_access_token(
                data={
                    "sub": str(user_data.userid),  # Assuming userid is the primary key
                    "email": user_data.email,
                    "role" : user_data.role
                },
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            return {
                "access_token": access_token, 
                "token_type": "bearer", 
                "user": user_data.userid,
                "role" : user_data.role,
                "message": "Credentials Verified"
            }
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=str(e)
            )
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

