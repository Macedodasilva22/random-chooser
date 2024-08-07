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
        document.getElementById('chat-response').innerText = data.response;
    })
    .catch(error => console.error('Error:', error));
});
