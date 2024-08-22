document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const message = document.getElementById('chat-input').value;

    // Show spinner wheel while randomizing
    document.getElementById('spinner-wheel').style.display = 'block';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Hide spinner wheel after randomization
        document.getElementById('spinner-wheel').style.display = 'none';
        handleChatResponse(data);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('spinner-wheel').style.display = 'none';
    });
});

function handleChatResponse(data) {
    const chatResponse = document.getElementById('chat-response');
    if (data.next_state === 1) {
        showOptionsInput(data.response);
    } else {
        chatResponse.innerText = data.response || 'No response from server.';
    }
}

function showOptionsInput(prompt) {
    const chatResponse = document.getElementById('chat-response');
    chatResponse.innerText = prompt;

    const chatInput = document.getElementById('chat-input');
    chatInput.value = '';
    chatInput.placeholder = 'Type your options here, one per line...';
    chatInput.rows = 5;

    const optionsInput = document.getElementById('options-input');
    optionsInput.style.display = 'block';

    const submitOptionsButton = document.getElementById('submit-options');
    submitOptionsButton.addEventListener('click', submitOptions);
}

function submitOptions() {
    const optionsText = document.getElementById('options-textarea').value;

    // Show spinner wheel during randomization
    document.getElementById('spinner-wheel').style.display = 'block';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: optionsText })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('spinner-wheel').style.display = 'none';
        document.getElementById('chat-response').innerText = data.response || 'No response from server.';

        const chatInput = document.getElementById('chat-input');
        chatInput.value = '';
        chatInput.placeholder = 'Type your dilemma here...';
        chatInput.rows = 4;

        const optionsInput = document.getElementById('options-input');
        optionsInput.style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('spinner-wheel').style.display = 'none';
    });
}
