import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from services.board import update_board
from services.connections import manager

app = FastAPI()



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            receive_data = await websocket.receive_json()
            await update_board(receive_data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Player left the game")


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
