from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.types import SocketType

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

users = {}

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()
    username = data["Authorization"]
    users[username] = websocket

    await broadcast_user_list()
    try:
        while True:
            data = await websocket.receive_json()
            await broadcast_events(data)
    except WebSocketDisconnect:
        del users[username]
        await broadcast_user_list()


async def broadcast_user_list():
    user_list = list(users.keys())
    for user in users.values():
        await user.send_json({"type": SocketType.UPDATE_USERS.value, "body": {"users": ','.join(user_list)}})

async def broadcast_events(data):
    body = data["body"]
    if data["type"] == SocketType.SEND_MESSAGE.value:
        await users[body["recipient"]].send_json({"type": SocketType.SEND_MESSAGE.value, "body": {"message": body["message"]}})

