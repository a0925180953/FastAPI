from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "secret"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60


def create_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # 🔥 測試帳密（先簡單）
    if username != "test" or password != "1234":
        raise HTTPException(status_code=400, detail="帳密錯誤")

    token = create_token({"sub": username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }