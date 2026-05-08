import json, os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from openai import OpenAI
from google import genai

from backend.ws.manager import manager
from backend.config import OPENAI_API_KEY, GEMINI_API_KEY
from backend.database import SessionLocal, get_db
from backend.models.models import Message

router = APIRouter()

openai_client = OpenAI(api_key=OPENAI_API_KEY)
genai_client = genai.Client(api_key=GEMINI_API_KEY)

@router.get("/history")
async def get_chat_history(channel: str = "general", db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.channel == channel).order_by(Message.timestamp.asc()).all()
    return [{"user": m.sender, "message": m.content, "time": m.timestamp} for m in messages]

@router.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await manager.connect(websocket, channel)
    db = SessionLocal()

    try:
        while True:
            data = await websocket.receive_text()
            print(f"收到 [{channel}]:", data)
            msg = json.loads(data)
            
            # 1. 儲存使用者訊息
            user_msg = Message(channel=channel, sender="User", content=msg["message"])
            db.add(user_msg)
            db.commit()

            # 只有在 ai-chat 頻道才觸發 AI 回覆
            if channel == "ai-chat":
                ai_reply = await ask_ai_gemini(msg["message"])
                
                # 3. 儲存 AI 訊息
                ai_msg = Message(channel=channel, sender="AI", content=ai_reply)
                db.add(ai_msg)
                db.commit()

                response = {
                    "user": "AI",
                    "message": ai_reply
                }
                await manager.broadcast(json.dumps(response), channel)
            else:
                # 一般頻道就只是廣播使用者訊息
                response = {
                    "user": "User",
                    "message": msg["message"]
                }
                await manager.broadcast(json.dumps(response), channel)

    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
    finally:
        db.close()

async def ask_ai_gpt(text):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred while generating GPT response: {e}")
        return "哈哈沒token,沒錢買token，可憐哪，快去買token吧！"

async def ask_ai_gemini(text):
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=text
        )
        return response.text
    except Exception as e:
        print(f"Error occurred while generating Gemini response: {e}")
        return "哈哈沒token,沒錢買token，可憐哪，快去買token吧！"
