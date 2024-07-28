
function sendMessage() {
    const userMessage = document.getElementById('user-message').value;
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const chatOutput = document.getElementById('chat-output');
        const userMessageP = document.createElement('p');
        userMessageP.innerHTML = `<strong>You:</strong> ${userMessage}`;
        const chatbotMessageP = document.createElement('p');
        chatbotMessageP.innerHTML = `<strong>ChatBot:</strong> ${data.response}`;
        chatOutput.appendChild(userMessageP);
        chatOutput.appendChild(chatbotMessageP);
        document.getElementById('user-message').value = '';

       
        if (data.chosen_option) {
            const chosenOptionDiv = document.getElementById('chosen-option');
            chosenOptionDiv.classList.remove('hidden');
            chosenOptionDiv.innerHTML = `ChatBot chose: <strong>${data.chosen_option}</strong>`;
            chosenOptionDiv.classList.add('win-animation'); 
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function clearHistory() {
    fetch('/clear-history', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const chatOutput = document.getElementById('chat-output');
        chatOutput.innerHTML = '';
        const chosenOptionDiv = document.getElementById('chosen-option');
        chosenOptionDiv.classList.add('hidden'); //
    })
    .catch(error => {
        console.error('Error clearing history:', error);
    });
}
