from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {} #словарь со всеми соединениями
        #обычно импортируется из бд

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int): 
        await websocket.accept() #подтверждение что чел может подключиться к данному вебсокету
        if room_id not in self.active_connections: #проверка о существовании комнаты
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket

    def disconnect(self, room_id: int, user_id: int):# Принимает WebSocket-соединение, идентификатор комнаты (room_id) и пользователя (user_id).
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]

    async def broadcast(self, message: str, room_id: int, sender_id: int):
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                message_with_class = {
                    "text": message,
                    "is_self": user_id == sender_id
                }
                await connection.send_json(message_with_class)

manager = ConnectionManager()
router = APIRouter(prefix="/ws/chat")
@router.websocket("/ws/{username}/{correspondent}")
async def websocket_endpoint(websocket: WebSocket, username: str, correspondent: str):
    await manager.connect(websocket, username, correspondent)
    await manager.broadcast(f"{username} присоединился к чату.", username, correspondent)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}", username, correspondent)
    except WebSocketDisconnect:
        manager.disconnect(username, correspondent)
        await manager.broadcast(f"{username} покинул чат.", username, correspondent)
#Конструктор класса

# self.active_connections — словарь, который хранит активные соединения, сгруппированные по комнатам (room_id).

# В каждой комнате (room_id) подключенные пользователи хранятся в виде {user_id: WebSocket}.

# connect


# Подтверждает соединение (websocket.accept()).

# Добавляет WebSocket в self.active_connections.

# disconnect

# Удаляет WebSocket пользователя из self.active_connections.

# Если в комнате не осталось пользователей, удаляет комнату.

# broadcast

# Отправляет сообщение всем пользователям в комнате.

# Дополнительно добавляет флаг is_self, чтобы клиент мог визуально выделять свои сообщения.

manager = ConnectionManager()
router = APIRouter(prefix="/ws/chat")


username = "ada"#это мы сразу будем получать когда зареганы,уже реаилизованно в основном коде

@router.websocket("/ws/{username}/{correspondent}")
async def websocket_endpoint(websocket: WebSocket, username: str, correspondent: str):
    if username == "ada":
        await manager.connect(websocket, username, correspondent)
        await manager.broadcast(f"{username} присоединился к чату.", username, correspondent)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"{username}: {data}", username, correspondent)
        except WebSocketDisconnect:
            manager.disconnect(username, correspondent)
            await manager.broadcast(f"{username} покинул чат.", username, correspondent)
#в этом файле надо сделать так чтоб ты подключался по 2 usernam'ам то есть нужно убрать все room_id

#--------------------------------------------------------------------------------------------------------------------------

#1. Функциональные требования
# 1.1. Пользовательские функции
# Регистрация и аутентификация:

# Пользователи должны иметь возможность регистрироваться и входить в систему.
# Поддержка аутентификации (например, с использованием JWT или OAuth).
# Создание и управление чатами:

# Возможность присоединяться и покидать чаты.
# Отправка и получение сообщений:

# Пользователи могут отправлять текстовые сообщения.
# Поддержка отправки медиафайлов (изображения, видео и т.д.).
# История сообщений:

# Хранение и отображение истории сообщений в чате.
# Возможность прокрутки вверх для просмотра старых сообщений.
# Уведомления:

# Уведомления о новых сообщениях для пользователей, находящихся в чате.
# Список участников:

# Отображение списка участников чата.
# 1.2. Административные функции
# Управление пользователями:
# Администраторы могут блокировать или удалять пользователей.
# Модерация чатов:
# Возможность удаления сообщений или блокировки пользователей в чате.
# 2. Нефункциональные требования
# Производительность:

# Чат должен поддерживать большое количество одновременных пользователей без значительных задержек.
# Безопасность:

# Защита данных пользователей и сообщений (шифрование, аутентификация).
# Защита от атак (например, XSS, CSRF).
# Масштабируемость:

# Возможность масштабирования приложения для поддержки увеличения числа пользователей.
# Доступность:

# Чат должен быть доступен 24/7 с минимальным временем простоя.
# 3. Алгоритм реализации
# 3.1. Архитектура
# Клиентская часть:

# Используйте фреймворк (например, React, Vue.js) для создания интерфейса пользователя.
# Реализуйте WebSocket для обмена сообщениями в реальном времени.
# Серверная часть:

# Используйте FastAPI для создания API и обработки WebSocket-соединений.
# Реализуйте базу данных (например, PostgreSQL, MongoDB) для хранения пользователей, чатов и сообщений.
# 3.2. Этапы реализации
# Настройка окружения:

# Установите необходимые библиотеки (FastAPI, Uvicorn, SQLAlchemy, Pydantic и т.д.).
# Настройте базу данных и создайте необходимые таблицы (пользователи, чаты, сообщения).
# Создание модели данных:

# Определите модели для пользователей, чатов и сообщений.
# Реализуйте миграции базы данных.
# Реализация аутентификации:

# Создайте эндпоинты для регистрации и входа в систему.
# Реализуйте JWT для аутентификации пользователей.
# Создание WebSocket-соединения:

# Реализуйте WebSocket-эндпоинт для обработки сообщений.
# Обработайте подключение, отключение и отправку сообщений.
# Создание API для управления чатами:

# Реализуйте эндпоинты для создания, получения и удаления чатов.
# Реализуйте эндпоинты для получения списка участников чата.
# Реализация клиентской части:

# Создайте интерфейс для регистрации, входа и управления чатами.
# Реализуйте функциональность отправки и получения сообщений через WebSocket.
# Тестирование:

# Проведите тестирование функциональности (юнит-тесты, интеграционные тесты).
# Проверьте производительность и безопасность приложения.
# Развертывание:

# Разверните приложение на сервере (например, Heroku, AWS, DigitalOcean).
# Настройте домен и SSL-сертификаты для безопасности.


#1. Удаление старых сообщений
# Политика хранения: Установите политику хранения сообщений, которая будет автоматически удалять старые сообщения через определенный период времени (например, 30 дней). Это можно сделать с помощью фонового задания или триггеров в базе данных.

# Пример SQL для удаления старых сообщений:
# DELETE FROM messages WHERE created_at < NOW() - INTERVAL '30 days';