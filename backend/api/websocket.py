import json, os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, status
from sqlalchemy.orm import Session
from openai import OpenAI
from google import genai
from jose import JWTError, jwt

from backend.ws.manager import manager
from backend.config import OPENAI_API_KEY, GEMINI_API_KEY, SECRET_KEY
from backend.database import SessionLocal, get_db
from backend.models.models import Message, User
from backend.utils.security import ALGORITHM

router = APIRouter()

openai_client = OpenAI(api_key=OPENAI_API_KEY)
genai_client = genai.Client(api_key=GEMINI_API_KEY)

DEFAULT_AVATAR = "https://api.dicebear.com/7.x/bottts/svg?seed=shinnosuke"

@router.get("/history")
async def get_chat_history(channel: str = "general", db: Session = Depends(get_db)):
    # 使用 join 取得使用者資訊
    messages = db.query(Message, User).outerjoin(User, Message.sender == User.username)\
        .filter(Message.channel == channel)\
        .order_by(Message.timestamp.asc()).all()
    
    result = []
    for m, u in messages:
        result.append({
            "user": m.sender,
            "nickname": u.nickname if u and u.nickname else m.sender,
            "avatar": u.avatar_url if u and u.avatar_url else DEFAULT_AVATAR,
            "message": m.content,
            "time": m.timestamp
        })
    return result

@router.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str, token: str = Query(None)):
    db = SessionLocal()
    current_user = None

    # 驗證 Token 並取得使用者
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username:
                current_user = db.query(User).filter(User.username == username).first()
        except JWTError:
            pass

    if not current_user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            msg_data = json.loads(data)
            msg_type = msg_data.get("type", "message")
            
            user_display_name = current_user.nickname or current_user.username
            user_avatar = current_user.avatar_url or DEFAULT_AVATAR

            if msg_type == "typing":
                typing_resp = {
                    "type": "typing",
                    "user": user_display_name,
                    "is_typing": msg_data.get("is_typing", False)
                }
                await manager.broadcast(json.dumps(typing_resp), channel)
                continue

            # 1. 儲存使用者訊息
            message_text = msg_data.get("message", "")
            user_msg = Message(channel=channel, sender=current_user.username, content=message_text)
            db.add(user_msg)
            db.commit()

            # 廣播使用者訊息
            if channel != "ai-chat":
                response = {
                    "type": "message",
                    "user": current_user.username,
                    "nickname": user_display_name,
                    "avatar": user_avatar,
                    "message": message_text
                }
                await manager.broadcast(json.dumps(response), channel)
            else:
                # AI 聊天頻道
                await manager.broadcast(json.dumps({
                    "type": "typing",
                    "user": "AI助理",
                    "is_typing": True
                }), channel)

                ai_reply = await ask_ai_gemini(message_text)
                
                ai_msg = Message(channel=channel, sender="AI", content=ai_reply)
                db.add(ai_msg)
                db.commit()

                await manager.broadcast(json.dumps({
                    "type": "typing",
                    "user": "AI助理",
                    "is_typing": False
                }), channel)

                await manager.broadcast(json.dumps({
                    "type": "message",
                    "user": "AI",
                    "nickname": "AI助理",
                    "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=AI",
                    "message": ai_reply
                }), channel)

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
