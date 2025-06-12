const input = document.getElementById("input");
const chatbox = document.getElementById("chatbox");
const micButton = document.createElement("button"); // Create a mic button
micButton.textContent = "🎤";
document.body.appendChild(micButton);

// Function to send message
function send() {
  const message = input.value;
  if (!message) return;
  appendMessage("You", message);
  input.value = "";

  fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message})
  })
  .then(res => res.json())
  .then(data => {
    appendMessage("Jarvis", data.reply);
    if (data.reply.includes("http")) window.open(data.reply.split(", ")[1], "_blank");
  });
}

// Function to append messages to the chatbox
function appendMessage(sender, text) {
  chatbox.innerHTML += `<p><strong>${sender}:</strong> ${text}</p>`;
  chatbox.scrollTop = chatbox.scrollHeight;
}

// Function to handle voice input using Web Speech API
let recognition;
function startVoiceRecognition() {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Your browser does not support voice recognition.");
    return;
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = function() {
    console.log("Voice recognition started...");
  };

  recognition.onerror = function(event) {
    console.error("Speech recognition error", event.error);
  };

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    input.value = transcript;
    send();
  };

  recognition.start();
}

// Activate voice recognition when the mic button is clicked
micButton.addEventListener("click", function() {
  startVoiceRecognition();
});
