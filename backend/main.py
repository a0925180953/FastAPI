import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.api import auth, websocket
from backend.database import engine, Base
from backend.utils.logger import backend_logger, frontend_logger
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

@asynccontextmanager
async def lifespan(app: FastAPI):

    # 【啟動部分】
    print("📢 [DEBUG] Lifespan 啟動了！")
    backend_logger.info("🚀 後端伺服器啟動成功！系統已就緒。")
    
    try:
        yield
    finally:
        # 【關閉部分】
        # 使用 print 測試是否真的有跑到這
        print("📢 [DEBUG] Lifespan 正在關閉...")
        backend_logger.info("🛌 後端伺服器已安全關閉。")
        
        # 手動強制沖刷日誌，而不是 shutdown
        for handler in backend_logger.handlers:
            handler.flush()

app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(websocket.router)

# 前端日誌模型
class FrontendLog(BaseModel):
    level: str = "error"
    message: str
    url: Optional[str] = None
    stack: Optional[str] = None

@app.post("/logs/frontend")
async def record_frontend_log(log: FrontendLog):
    log_msg = f"[{log.url}] {log.message}"
    if log.stack:
        log_msg += f"\nStack: {log.stack}"

    if log.level == "error":
        frontend_logger.error(log_msg)
    elif log.level == "warn":
        frontend_logger.warning(log_msg)
    else:
        frontend_logger.info(log_msg)

    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",  # 確保這裡的字串與你的目錄結構一致
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_config=None,      # 避免 Uvicorn 覆蓋你的 logger 設定
        timeout_graceful_shutdown=5
    )