let ws;
let userName;

function connect() {
    userName = document.getElementById("username").value;
    ws = new WebSocket(`ws://localhost:8000/ws`);
    ws.onopen = function() {
        ws.send(JSON.stringify({ Authorization: userName, body: {}, type: "" }));
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const body = data["body"]
        if (data["type"] === "UPDATE_USERS") {
            const users = body["users"].split(",");
            updateUserList(users);
        }
        if (data["type"] === "SEND_MESSAGE") {
            displayMessage(body["message"], false);
        }
    };
}

function sendMessage() {
    const recipient = document.getElementById("user-dropdown").value;
    const message = document.getElementById("message").value;
    ws.send(JSON.stringify({ body: {recipient, message}, type: "SEND_MESSAGE" }));
    displayMessage(message, true);
    document.getElementById("message").value = "";
}

function updateUserList(users) {
    const dropdown = document.getElementById("user-dropdown");
    dropdown.innerHTML = '';

    users.forEach(user => {
        if (user !== userName) {
            const option = document.createElement("option");
            option.value = user;
            option.textContent = user;
            dropdown.appendChild(option);
        }
    });
}

function displayMessage(message, isOutgoing) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.classList.add(isOutgoing ? "outgoing" : "incoming");
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
