document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const message = document.getElementById('chat-input').value;

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        handleChatResponse(data);
    })
    .catch(error => console.error('Error:', error));
});

function handleChatResponse(data) {
    const chatResponse = document.getElementById('chat-response');
    if (data.next_state === 1) {
        // Preparing for options input
        showOptionsInput(data.response);
    } else {
        // Displaying the response
        chatResponse.innerText = data.response || 'No response from server.';
    }
}

function showOptionsInput(prompt) {
    // Update the response and prepare for options input
    const chatResponse = document.getElementById('chat-response');
    chatResponse.innerText = prompt;
    
    // Update chat input field for options
    const chatInput = document.getElementById('chat-input');
    chatInput.value = '';
    chatInput.placeholder = 'Type your options here, one per line...';
    chatInput.rows = 5;

    // Show options input area
    const optionsInput = document.getElementById('options-input');
    optionsInput.style.display = 'block';
    
    // Prepare the submit button for options
    const submitOptionsButton = document.getElementById('submit-options');
    submitOptionsButton.addEventListener('click', submitOptions);
}

function submitOptions() {
    const optionsText = document.getElementById('options-textarea').value;
    
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: optionsText })
    })
    .then(response => response.json())
    .then(data => {
        // Display the response
        document.getElementById('chat-response').innerText = data.response || 'No response from server.';
        
        // Reset input field
        const chatInput = document.getElementById('chat-input');
        chatInput.value = '';
        chatInput.placeholder = 'Type your dilemma here...';
        chatInput.rows = 4;

        // Hide options input area
        const optionsInput = document.getElementById('options-input');
        optionsInput.style.display = 'none';
    })
    .catch(error => console.error('Error:', error));
}
