async function sendMessage() {
    // Get the user's message from the input field
    const message = document.getElementById('user-input').value;

    // Validate the message is not empty
    if (!message.trim()) {
        document.getElementById('response').innerText = 'Please enter a question.';
        return;
    }

    try {
        // Make a POST request to the Heroku backend
        const response = await fetch('https://whispering-journey-33686-b637147571a8.herokuapp.com/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any additional headers if needed
            },
            body: JSON.stringify({ question: message }),
        });

        // Check if the response is successful
        if (!response.ok) {
            // Extract and log error details
            const errorText = await response.text();
            throw new Error(`Network response was not ok. Status: ${response.status}. ${errorText}`);
        }

        // Parse and display the response data
        const data = await response.json();
        document.getElementById('response').innerText = data.answer || 'No answer received.';
    } catch (error) {
        // Log and display errors
        console.error('There was a problem with the request:', error);
        document.getElementById('response').innerText = 'Sorry, there was a problem with the request.';
    }
}

// Attach event listener to the button
document.getElementById('submit-button').addEventListener('click', sendMessage);
