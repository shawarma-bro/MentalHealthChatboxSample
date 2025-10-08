function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    
    if (!message) return; // Prevent empty messages

    const chatBox = document.getElementById("chat-box");

    // Append user message to chatbox
    chatBox.innerHTML += `<div class="user">You: ${message}</div>`;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response from server:", data); // Debugging line
        chatBox.innerHTML += `<div class="bot">Bot: ${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    
        // Change UI based on mood
        updateMoodUI(data.mood);
    });
    
    })
    .catch(error => {
        console.error("Error:", error);
        chatBox.innerHTML += `<div class="bot">Bot: Something went wrong. Try again!</div>`;
    });

    input.value = ''; // Clear input after sending
}

function updateMoodUI(mood) {
    const chatBox = document.getElementById("chat-box");

    if (!mood) {
        console.warn("No mood received, skipping UI update.");
        return; // Prevent errors if mood is undefined
    }

    const body = document.body;

    switch (mood) {
        case "positive":
            body.style.backgroundColor = "#d4f8d4"; // Light Green
            chatBox.style.backgroundColor = "#ffffff"; 
            break;
        case "negative":
            body.style.backgroundColor = "#f8dada"; // Light Red
            chatBox.style.backgroundColor = "#fff3f3"; 
            break;
        default:
            body.style.backgroundColor = "#f4f4f9"; // Default neutral
            chatBox.style.backgroundColor = "#ffffff";
            break;
    }

    console.log("Updated UI to mood:", mood); // Debugging line
}


