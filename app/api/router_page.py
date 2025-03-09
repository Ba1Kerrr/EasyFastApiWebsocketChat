from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory='app/templates')
router = APIRouter()
users = [
  {"username": "adada"},
  {"username": "ada"},
  {"username": "qwerty"},
  {"username": "asdfgh"},
  {"username": "zxcvbn"},
  {"username": "qweasd"},
  {"username": "ytrewq"},
  {"username": "poiuyt"},
  {"username": "lkjhgf"},
  {"username": "mnbvcx"}
]
# смотри,для 2х пользователей мы должны реализовать фичу которая создает для них 1 комнату по хэшам их ников

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("page.html", {"request": request,"users":users})

@router.post("/take_link", response_class=HTMLResponse)
async def join_chat(request: Request, username: str = "ada", correspondent: str = Form(...)):
    if username < correspondent:
        room_id = f"{username}-{correspondent}" 
    else :
        room_id = f"{correspondent}-{username}"
    
    return templates.TemplateResponse("page.html",
                                      {"request": request,"room_id": room_id,"username": username,"correspondent": correspondent})

# @router.get("/", response_class=HTMLResponse)
# async def home_page(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})


# @router.post("/join_chat", response_class=HTMLResponse)
# async def join_chat(request: Request, username: str = Form(...), correspondent: str = Form(...)):
#     # Простая генерация user_id
#     user_id = hash(username) % 10000
#     correspondent_id = hash(correspondent) % 10000
#     room_id = f"{user_id}-{correspondent_id}"
#     return templates.TemplateResponse("index.html",
#                                       {"request": request,"room_id": room_id,"username": username,"user_id": user_id})