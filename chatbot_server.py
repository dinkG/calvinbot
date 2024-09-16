from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/chat": {"origins": "*"}})

# Define the API Gateway URL (replace this with your actual endpoint)
API_URL = "https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/"

@app.route('/')
def home():
    return "John Calvin Chatbot API is running!"

# Define the chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    # Get the request data (user's question)
    data = request.get_json()

    # Check if the 'question' is in the data
    if 'question' not in data:
        return jsonify({"error": "No question provided"}), 400

    # Get the user's question
    user_question = data['question']
    
    try:
        # Make a POST request to the AWS Lambda API Gateway
        response = requests.post(API_URL, json={"user_query": user_question})

        # Check if the response was successful
        if response.status_code == 200:
            result = response.json()
            # Get the answer from the API response
            answer = result.get('Answer', "I don't have an answer for you")
            return jsonify({"answer": answer})
        else:
            # Handle the case where the API returns a non-200 status code
            return jsonify({
                "error": "Error from API",
                "status_code": response.status_code,
                "response": response.text
            }), 500

    except requests.exceptions.RequestException as e:
        # Handle network errors
        return jsonify({"error": "API request failed", "message": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    # Make the app accessible externally via 0.0.0.0
    app.run(host='0.0.0.0', port=5001)
