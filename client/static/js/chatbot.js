document.addEventListener("DOMContentLoaded", () => {
  const chatbotIcon = document.getElementById("chatbotIcon");
  const chatPopup = document.getElementById("chatPopup");
  const closeChat = document.getElementById("closeChat");
  const sendBtn = document.getElementById("sendBtn");
  const userInput = document.getElementById("userInput");
  const chatBody = document.getElementById("chatBody");

  const API_URL = "/chatbot/get_response"; 

  // Open chatbot popup
  chatbotIcon.addEventListener("click", () => {
    chatPopup.classList.add("active");
    userInput.focus();
    chatBody.innerHTML = `<div class="nurse-msg"><b>Nurse:</b> Hi 👩‍⚕️ How can I help you today?</div>`;
    scrollChatToBottom();
  });

  // Close chatbot popup
  closeChat.addEventListener("click", () => {
    chatPopup.classList.remove("active");
    chatBody.innerHTML = "";
    userInput.value = "";
  });

  // Send message on Enter key
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // Send message on button click
  sendBtn.addEventListener("click", sendMessage);

  function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("You", message, "user");
    userInput.value = "";

    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("nurse-msg");
    typingIndicator.innerHTML = `<b>Nurse:</b> <i>Typing...</i>`;
    chatBody.appendChild(typingIndicator);
    scrollChatToBottom();

    // Fetch response from Flask backend
    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    })
      .then((res) => res.json())
      .then((data) => {
        typingIndicator.remove(); 
        appendMessage("Nurse", data.response, "nurse");
      })
      .catch((err) => {
        typingIndicator.remove();
        appendMessage("Nurse", "⚠️ Something went wrong. Please try again.", "nurse");
        console.error("Chatbot Error:", err);
      });
  }

  function appendMessage(sender, message, type) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add(`${type}-msg`);
    msgDiv.innerHTML = `<b>${sender}:</b> ${message}`;
    chatBody.appendChild(msgDiv);
    scrollChatToBottom();
  }

  function scrollChatToBottom() {
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});
