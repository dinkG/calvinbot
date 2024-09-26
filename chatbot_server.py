from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
import json

app = Flask(__name__)

# Allow CORS for specific origin with necessary headers and support for preflight requests
CORS(app, resources={r"/chat": {"origins": "https://theologiananswers.com"}}, supports_credentials=True)

# Define the API URLs for different theologians from environment variables or default URLs
API_URL_CALVIN = os.getenv('API_URL_CALVIN', 'https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/')
API_URL_AUGUSTINE = os.getenv('API_URL_AUGUSTINE', 'https://augustine-api.com/dev/')
API_URL_AQUINAS = os.getenv('API_URL_AQUINAS', 'https://aquinas-api.com/dev/')
API_URL_LUTHER = os.getenv('API_URL_LUTHER', 'https://co9rp2odta.execute-api.us-east-1.amazonaws.com/Dev/')
API_URL_EDWARDS = os.getenv('API_URL_EDWARDS', 'https://edwards-api.com/dev/')

# Directory to store articles
ARTICLES_DIR = './articles'

# Mapping of specific S3 URLs to new URLs
URL_REPLACEMENTS = {
    "s3://lutherbot/bondage.txt": "https://partner.logosbible.com/click.track?CID=432198&AFID=564576&nonencodedurl=https://www.logos.com/product/149302/the-bondage-of-the-will"
}

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return _build_cors_prelight_response()
    
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
            citation = result.get('Citation', '')

            # Replace the citation if it matches any in the URL_REPLACEMENTS
            if citation in URL_REPLACEMENTS:
                citation = URL_REPLACEMENTS[citation]

            # Add the citation to the end of the answer if it exists
            if citation:
                answer += f"\n\nSource: {citation}"

            # Create an article using the question and answer
            create_article(user_question, theologian, answer)

            return _build_cors_actual_response(jsonify({"answer": answer}))
        else:
            return _build_cors_actual_response(jsonify({
                "error": "Error from API",
                "status_code": response.status_code,
                "response": response.text
            }), 500)

    except requests.exceptions.RequestException as e:
        return _build_cors_actual_response(jsonify({"error": "API request failed", "message": str(e)}), 500)

def create_article(question, theologian, answer):
    """
    Create an article and save it to the articles directory.
    """
    try:
        if not os.path.exists(ARTICLES_DIR):
            os.makedirs(ARTICLES_DIR)
        
        # Prepare the article data
        article = {
            "title": f"{theologian.capitalize()} on: {question}",
            "content": answer
        }

        # Define a unique filename for the article
        filename = os.path.join(ARTICLES_DIR, f"{theologian}_{len(os.listdir(ARTICLES_DIR)) + 1}.json")

        # Write the article to a JSON file
        with open(filename, 'w') as file:
            json.dump(article, file)
    except Exception as e:
        print(f"Failed to create article: {e}")

@app.route('/articles', methods=['GET'])
def get_articles():
    """
    Retrieve all articles in the articles directory.
    """
    try:
        articles = []
        for filename in os.listdir(ARTICLES_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(ARTICLES_DIR, filename), 'r') as file:
                    article = json.load(file)
                    articles.append(article)
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to handle CORS preflight responses
def _build_cors_prelight_response():
    response = jsonify({"message": "CORS preflight success"})
    response.headers.add("Access-Control-Allow-Origin", "https://theologiananswers.com")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

# Function to add CORS headers to actual responses
def _build_cors_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "https://theologiananswers.com")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
