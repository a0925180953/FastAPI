import json, os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.ws.manager import manager
from backend.config import OPENAI_API_KEY, GEMINI_API_KEY
from openai import OpenAI

router = APIRouter()
openai_client = OpenAI(api_key=OPENAI_API_KEY)

from google import genai
client = genai.Client(api_key=GEMINI_API_KEY)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print("收到:", data)
            msg = json.loads(data)
            ai_reply = await ask_ai_gemini(msg["message"])
            response = {
                "user": "AI",
                "message": ai_reply
            }
            await manager.broadcast(json.dumps(response))

    except WebSocketDisconnect:
        manager.disconnect(websocket)

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
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=text
        )
        return response.text
    except Exception as e:
        print(f"Error occurred while generating Gemini response: {e}")
        return "哈哈沒token,沒錢買token，可憐哪，快去買token吧！"