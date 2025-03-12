let ws; // Переменная для хранения WebSocket соединения
let userName; // Переменная для хранения имени пользователя

function connect() {
    // Получаем имя пользователя из поля ввода
    userName = document.getElementById("username").value;
    // Создаем новое WebSocket соединение с указанным адресом
    ws = new WebSocket("ws://localhost:8000/ws");
    
    // Устанавливаем обработчик, который сработает, когда соединение открыто
    ws.onopen = function() {
        // Отправляем сообщение на сервер с именем пользователя
        ws.send(JSON.stringify({ Authorization: userName, body: {}, type: "" }));
    };

    // Устанавливаем обработчик для получения сообщений от сервера
    ws.onmessage = function(event) {
        // Парсим полученные данные из сообщения
        const data = JSON.parse(event.data);
        const body = data["body"]; // Извлекаем тело сообщения
        
        // Проверяем тип полученного сообщения
        if (data["type"] === "UPDATE_USERS") {
            // Если тип сообщения - обновление пользователей, разбиваем строку на массив
            const users = body["users"].split(",");
            // Обновляем список пользователей
            updateUserList(users);
        }
        
        // Проверяем тип сообщения для отправленного сообщения
        if (data["type"] === "SEND_MESSAGE") {
            // Если это сообщение, отображаем его в чате
            displayMessage(body["message"], false);
        }
    };
}

function sendMessage() {
    // Получаем выбранного получателя из выпадающего списка
    const recipient = document.getElementById("user-dropdown").value;
    // Получаем текст сообщения из поля ввода
    const message = document.getElementById("message").value;
    
    // Отправляем сообщение получателю через WebSocket
    ws.send(JSON.stringify({ body: {recipient, message}, type: "SEND_MESSAGE" }));
    // Отображаем сообщение в чате как исходящее
    displayMessage(message, true);
    // Очищаем поле ввода после отправки
    document.getElementById("message").value = "";
}

function updateUserList(users) {
    // Получаем ссылку на выпадающий список для пользователей
    const dropdown = document.getElementById("user-dropdown");
    // Очищаем текущий список пользователей
    dropdown.innerHTML = '';

    // Проходим по массиву пользователей и добавляем их в выпадающий список
    users.forEach(user => {
        // Не добавляем себя в список пользователей
        if (user !== userName) {
            // Создаем новый элемент option для выпадающего списка
            const option = document.createElement("option");
            option.value = user; // Устанавливаем значение для option
            option.textContent = user; // Устанавливаем текст для option
            // Добавляем option в выпадающий список
            dropdown.appendChild(option);
        }
    });
}

function displayMessage(message, isOutgoing) {
    // Получаем ссылку на элемент, где будут отображаться сообщения
    const chatBox = document.getElementById("chat-box");
    // Создаем новый элемент для сообщения
    const messageElement = document.createElement("div");
    messageElement.classList.add("message"); // Добавляем общий класс для сообщения
    // Добавляем класс в зависимости от того, исходящее это сообщение или входящее
    messageElement.classList.add(isOutgoing ? "outgoing" : "incoming");
    messageElement.textContent = message; // Добавляем текст сообщения к элементу
    // Добавляем элемент сообщения в чат
    chatBox.appendChild(messageElement);
    // Прокручиваем чат к последнему сообщению
    chatBox.scrollTop = chatBox.scrollHeight;
}