from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # 結構: { "channel_name": [websocket1, websocket2] }
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.rooms:
            if websocket in self.rooms[room]:
                self.rooms[room].remove(websocket)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, message: str, room: str):
        if room in self.rooms:
            for connection in self.rooms[room]:
                await connection.send_text(message)

manager = ConnectionManager()
