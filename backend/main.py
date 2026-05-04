import os
from dotenv import load_dotenv
from fastapi import FastAPI
from backend.api import auth, websocket
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

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