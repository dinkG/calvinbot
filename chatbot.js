async function sendMessage() {
    // Get the user's message from the input field
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    const theologian = document.getElementById('theologian-select').value;

    // Validate the message is not empty
    if (!message) {
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
            body: JSON.stringify({
                question: message,
                theologian: theologian  // Pass the selected theologian
            }),
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

    // Clear input field
    inputField.value = '';
    // Update chat background based on selected theologian
    updateChatBackground();
}

// Attach event listener to the button
document.getElementById('submit-button').addEventListener('click', sendMessage);

function updateChatBackground() {
    const theologian = document.getElementById('theologian-select').value;
    const messagesContainer = document.getElementById('messages');

    // Remove any existing theologian background classes
    messagesContainer.className = 'messages';
    
    // Add the background class based on the selected theologian
    switch (theologian) {
        case 'calvin':
            messagesContainer.classList.add('bg-calvin');
            break;
        case 'augustine':
            messagesContainer.classList.add('bg-augustine');
            break;
        case 'aquinas':
            messagesContainer.classList.add('bg-aquinas');
            break;
        case 'luther':
            messagesContainer.classList.add('bg-luther');
            break;
        case 'edwards':
            messagesContainer.classList.add('bg-edwards');
            break;
        default:
            messagesContainer.classList.add('bg-calvin'); // Default background if no theologian selected
    }

    // Trigger a reflow to apply the transition
    messagesContainer.offsetHeight; // Trigger a reflow
    messagesContainer.querySelector('::before').style.opacity = 1;
}
