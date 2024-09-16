from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

API_URL = os.getenv('API_URL', 'https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if 'question' not in data:
        return jsonify({"error": "No question provided"}), 400

    user_question = data['question']
    try:
        response = requests.post(API_URL, json={"user_query": user_question})
        if response.status_code == 200:
            result = response.json()
            answer = result.get('Answer', 'No response available from API.')
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
