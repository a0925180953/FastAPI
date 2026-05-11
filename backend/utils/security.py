from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from backend.config import SECRET_KEY

SECRET_KEY = SECRET_KEY
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode.update({"exp": expires_at})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)