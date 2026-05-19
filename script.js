const input = document.querySelector("#commandInput");
const button = document.querySelector("#sendCommand");
const conversation = document.querySelector("#conversation");

const demoReplies = [
  "I will capture the request, identify the intent, and suggest the safest next action.",
  "That can become a voice command with speech-to-text, AI reasoning, and text-to-speech output.",
  "For production, I would add permissions before running tools that change files or accounts."
];

let replyIndex = 0;

function addMessage(text, type) {
  const message = document.createElement("article");
  message.className = `message ${type}`;
  message.textContent = text;
  conversation.append(message);
  message.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function runDemoCommand() {
  const command = input.value.trim();
  if (!command) {
    input.focus();
    return;
  }

  addMessage(command, "user");
  addMessage(demoReplies[replyIndex], "assistant");
  replyIndex = (replyIndex + 1) % demoReplies.length;
  input.value = "";
}

button.addEventListener("click", runDemoCommand);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    runDemoCommand();
  }
});
