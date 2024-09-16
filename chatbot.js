async function sendMessage() {
    const message = document.getElementById('messageInput').value;
    try {
        const response = await fetch('https://whispering-journey-33686-b637147571a8.herokuapp.com/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const data = await response.json();
        document.getElementById('response').innerText = data.answer || 'No answer received.';
    } catch (error) {
        console.error('There was a problem with the request:', error);
        document.getElementById('response').innerText = 'Sorry, there was a problem with the request.';
    }
}
