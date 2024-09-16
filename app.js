document.getElementById("send-button").addEventListener("click", function() {
    sendMessage();
});

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (message) {
        // Add user message to chat
        addMessageToChat("user", message);
        
        // Clear the input field
        inputField.value = "";

        // Send message to server
        fetch("http://localhost:5001/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: message })
        })
        .then(response => response.json())
        .then(data => {
            // Add bot response to chat
            addMessageToChat("bot", data.answer);
        })
        .catch(error => {
            console.error("Error:", error);
            addMessageToChat("bot", "Sorry, an error occurred.");
        });
    }
}

function addMessageToChat(sender, message) {
    const chatBox = document.getElementById("messages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);

    // Scroll to the bottom of the chat
    chatBox.scrollTop = chatBox.scrollHeight;
}
