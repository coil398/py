from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter, HTTPException

app = FastAPI()
router = APIRouter()
app.include_router(router)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    # Authorization check
    token = websocket.headers.get("Authorization")
    if token != "valid_token":
        await websocket.close(code=1008)
        raise HTTPException(status_code=403, detail="Unauthorized access")

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("client left")
