from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import BaseModel
from backend.database import get_db
from backend.models.models import User
from backend.schemas import UserCreate, UserUpdate, UserRead
from backend.utils.security import hash_password, verify_password, create_token, ALGORITHM
from backend.config import SECRET_KEY

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="找不到登入資訊，請重新登入。",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserRead)
def update_user_me(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 如果有要更新暱稱
    if user_update.nickname is not None:
        current_user.nickname = user_update.nickname
    
    # 如果有要更新大頭貼
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url
    
    # 如果有要更新密碼
    if user_update.password is not None:
        current_user.password = hash_password(user_update.password)
        
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 檢查使用者是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="此帳號已被註冊，請嘗試其他名稱。")

    # 建立新使用者
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "註冊成功！歡迎加入，請前往登入。"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 查找使用者
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤，請再試一次。")

    token = create_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

class PasswordReset(BaseModel):
    username: str
    email: str
    new_password: str

@router.post("/reset-password")
def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username, User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="找不到對應的帳號或 Email，請重新檢查。")
    
    user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "密碼重設成功！請使用新密碼登入。"}
