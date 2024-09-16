from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable CORS for the specified origin
CORS(app, resources={r"/chat": {"origins": "http://theologiananswers.com"}})

# Define the API URL from an environment variable or use a default one
API_URL = os.getenv('API_URL', 'https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/')

@app.route('/chat', methods=['POST'])
def chat():
    # Get the JSON data from the request
    data = request.get_json()

    # Check if 'question' is in the data
    if 'question' not in data:
        return jsonify({"error": "No question provided"}), 400

    # Extract the user's question
    user_question = data['question']
    
    try:
        # Make a POST request to the external API
        response = requests.post(API_URL, json={"user_query": user_question})

        # Check if the response from the API is successful
        if response.status_code == 200:
            result = response.json()
            # Get the answer from the API response
            answer = result.get('Answer', 'No response available from API.')
            return jsonify({"answer": answer})
        else:
            # Return an error response if the API call was not successful
            return jsonify({
                "error": "Error from API",
                "status_code": response.status_code,
                "response": response.text
            }), 500

    except requests.exceptions.RequestException as e:
        # Handle and return network errors
        return jsonify({"error": "API request failed", "message": str(e)}), 500

if __name__ == '__main__':
    # Get the port from environment variables or use default 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
