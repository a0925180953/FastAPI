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
            msg_data = json.loads(data)
            
            msg_type = msg_data.get("type", "message")
            
            if msg_type == "typing":
                # 廣播使用者正在輸入的狀態給其他人
                typing_resp = {
                    "type": "typing",
                    "user": "User",  # 這裡建議以後可以帶入使用者名稱
                    "is_typing": msg_data.get("is_typing", False)
                }
                await manager.broadcast(json.dumps(typing_resp), channel)
                continue

            # 1. 儲存使用者訊息
            message_text = msg_data.get("message", "")
            user_msg = Message(channel=channel, sender="User", content=message_text)
            db.add(user_msg)
            db.commit()

            # 一般頻道廣播使用者訊息
            if channel != "ai-chat":
                response = {
                    "type": "message",
                    "user": "User",
                    "message": message_text
                }
                await manager.broadcast(json.dumps(response), channel)
            else:
                # 只有在 ai-chat 頻道才觸發 AI 回覆
                # 先發送 AI 正在輸入的狀態
                await manager.broadcast(json.dumps({
                    "type": "typing",
                    "user": "AI",
                    "is_typing": True
                }), channel)

                ai_reply = await ask_ai_gemini(message_text)
                
                # 3. 儲存 AI 訊息
                ai_msg = Message(channel=channel, sender="AI", content=ai_reply)
                db.add(ai_msg)
                db.commit()

                # 發送 AI 訊息並取消輸入狀態
                await manager.broadcast(json.dumps({
                    "type": "typing",
                    "user": "AI",
                    "is_typing": False
                }), channel)

                response = {
                    "type": "message",
                    "user": "AI",
                    "message": ai_reply
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
        return "你賴東東不錯嘛~"

async def ask_ai_gemini(text):
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=text
        )
        return response.text
    except Exception as e:
        print(f"Error occurred while generating Gemini response: {e}")
        return "你賴東東不錯嘛~"
