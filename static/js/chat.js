const chatBody = document.getElementById("chat-body");
const input = document.getElementById("user-message");

/* Add message to chat */
function addMessage(text, sender = "bot") {
  const msg = document.createElement("div");
  msg.classList.add("chat-message", sender);

  const bubble = document.createElement("div");
  bubble.classList.add("chat-bubble");
  bubble.innerText = text;

  msg.appendChild(bubble);
  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;
}

/* Typing indicator */
function showTyping() {
  const typing = document.createElement("div");
  typing.classList.add("chat-message", "bot");
  typing.id = "typing-indicator";

  const bubble = document.createElement("div");
  bubble.classList.add("chat-bubble", "typing");
  bubble.innerText = "Assistant is typing...";

  typing.appendChild(bubble);
  chatBody.appendChild(typing);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById("typing-indicator");
  if (typing) typing.remove();
}

/* Send message to Flask chatbot */
async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  showTyping();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    removeTyping();

    addMessage(data.reply || "No response from assistant.", "bot");

  } catch (error) {
    removeTyping();
    addMessage("Error connecting to chatbot service.", "bot");
    console.error(error);
  }
}

/* Enter key support */
document.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && document.activeElement === input) {
    sendMessage();
  }
});
