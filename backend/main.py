import os
from fastapi import FastAPI
from backend.api import auth, websocket
from backend.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("KEY:", OPENAI_API_KEY)
print("GEMINI_KEY:", GEMINI_API_KEY)
app.include_router(auth.router)
app.include_router(websocket.router)