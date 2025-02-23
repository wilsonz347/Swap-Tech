document.getElementById('chat-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const questionInput = document.getElementById('question-input');
    const fileInput = document.getElementById('file-input');
    const chatBox = document.getElementById('chat-box');

    const question = questionInput.value.trim();
    const file = fileInput.files[0];

    if (!question) {
        alert('Please enter a question.');
        return;
    }

    // Display user's question in the chat box
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = `You: ${question}`;
    chatBox.appendChild(userMessage);

    // Clear the input field
    questionInput.value = '';

    // Prepare form data
    const formData = new FormData();
    formData.append('question', question);
    if (file) {
        formData.append('file', file);
    }

    try {
        // Send the request to the backend
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            // Display the chatbot's response in the chat box
            const botMessage = document.createElement('div');
            botMessage.classList.add('message', 'bot-message');
            botMessage.textContent = `Bot: ${data.answer}`;
            chatBox.appendChild(botMessage);
        } else {
            // Display an error message
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('message', 'bot-message');
            errorMessage.textContent = `Error: ${data.error}`;
            chatBox.appendChild(errorMessage);
        }
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('message', 'bot-message');
        errorMessage.textContent = 'Error: Unable to connect to the server.';
        chatBox.appendChild(errorMessage);
    }

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
});