from passlib.context import CryptContext
from datetime import datetime, timedelta
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from jose import jwt
import os
from app.config import settings
from pydantic import BaseModel, EmailStr
from app.users.dao import UsersDAO


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(pain_password, hashed_password) -> bool:
    return pwd_context.verify(pain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM 
        )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_by_one_or_none(email=email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user