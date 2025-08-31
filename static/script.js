document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.querySelector("button");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  sendButton.addEventListener("click", () => {
    const message = userInput.value.trim();
    if (!message) return;

    // Display user message
    const userMsg = document.createElement("div");
    userMsg.classList.add("user-message");
    userMsg.textContent = message;
    chatBox.appendChild(userMsg);
    userInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send message to Flask backend
    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    })
      .then(response => response.json())
      .then(data => {
        const botMsg = document.createElement("div");
        botMsg.classList.add("bot-message");
        botMsg.textContent = data.reply;
        chatBox.appendChild(botMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch(error => {
        console.error("Error:", error);
      });
  });

  
  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      sendButton.click();
    }
  });
});
