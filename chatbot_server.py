from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)

# Allow requests from a specific origin
CORS(app, resources={r"/chat": {"origins": "http://theologiananswers.com"}})

# Define the API URLs for different theologians from environment variables or default URLs
API_URL_CALVIN = os.getenv('API_URL_CALVIN', 'https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/')
API_URL_AUGUSTINE = os.getenv('API_URL_AUGUSTINE', 'https://augustine-api.com/dev/')
API_URL_AQUINAS = os.getenv('API_URL_AQUINAS', 'https://aquinas-api.com/dev/')
API_URL_LUTHER = os.getenv('API_URL_LUTHER', 'https://co9rp2odta.execute-api.us-east-1.amazonaws.com/Dev/')
API_URL_EDWARDS = os.getenv('API_URL_EDWARDS', 'https://edwards-api.com/dev/')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if 'question' not in data or 'theologian' not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_question = data['question']
    theologian = data['theologian']
    
    try:
        # Handle different theologians by calling the appropriate API
        if theologian == 'calvin':
            response = requests.post(API_URL_CALVIN, json={"user_query": user_question})
        elif theologian == 'augustine':
            response = requests.post(API_URL_AUGUSTINE, json={"user_query": user_question})
        elif theologian == 'aquinas':
            response = requests.post(API_URL_AQUINAS, json={"user_query": user_question})
        elif theologian == 'luther':
            response = requests.post(API_URL_LUTHER, json={"user_query": user_question})
        elif theologian == 'edwards':
            response = requests.post(API_URL_EDWARDS, json={"user_query": user_question})
        else:
            return jsonify({"error": "Unknown theologian selected"}), 400

        # Check for successful response from the API
        if response.status_code == 200:
            result = response.json()
            answer = result.get('Answer', 'No response available from the API.')
            return jsonify({"answer": answer})
        else:
            return jsonify({
                "error": "Error from API",
                "status_code": response.status_code,
                "response": response.text
            }), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "API request failed", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
