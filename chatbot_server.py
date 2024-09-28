from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import pymysql

app = Flask(__name__)

# Allow CORS for all routes from 'https://theologiananswers.com'
CORS(app, resources={r"/*": {"origins": "https://theologiananswers.com"}}, supports_credentials=True)

# Define the API URLs for different theologians from environment variables or default URLs
API_URL_CALVIN = os.getenv('API_URL_CALVIN', 'https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/')
API_URL_AUGUSTINE = os.getenv('API_URL_AUGUSTINE', 'https://augustine-api.com/dev/')
API_URL_AQUINAS = os.getenv('API_URL_AQUINAS', 'https://aquinas-api.com/dev/')
API_URL_LUTHER = os.getenv('API_URL_LUTHER', 'https://co9rp2odta.execute-api.us-east-1.amazonaws.com/Dev/')
API_URL_EDWARDS = os.getenv('API_URL_EDWARDS', 'https://edwards-api.com/dev/')

# Database connection details
DB_HOST = 'articles-db.c3wekyg2gws1.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'Flop56!!'
DB_NAME = 'theologian_chatbot'

# Helper function to connect to the database
def connect_to_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Route to handle chat requests
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

            # Store the interaction as an article in the database
            article_title = f"{theologian}: {user_question}"
            store_article(article_title, answer)

            # Return the response
            return _build_cors_actual_response(jsonify({"answer": answer}))
        else:
            return _build_cors_actual_response(jsonify({
                "error": "Error from API",
                "status_code": response.status_code,
                "response": response.text
            }), 500)

    except requests.exceptions.RequestException as e:
        return _build_cors_actual_response(jsonify({"error": "API request failed", "message": str(e)}), 500)

# Function to store an article in the database
def store_article(title, content):
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = "INSERT INTO articles (title, content) VALUES (%s, %s)"
            cursor.execute(sql, (title, content))
        connection.commit()
    except Exception as e:
        print(f"Error storing article: {e}")
    finally:
        connection.close()

# Route to fetch articles from the database
@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = "SELECT title, content FROM articles"
            cursor.execute(sql)
            articles = cursor.fetchall()
        return _build_cors_actual_response(jsonify(articles))
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return jsonify({"error": "Error fetching articles"}), 500
    finally:
        connection.close()

# Function to handle CORS preflight responses
def _build_cors_prelight_response():
    response = jsonify({"message": "CORS preflight success"})
    response.headers.add("Access-Control-Allow-Origin", "https://theologiananswers.com")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
    return response

# Function to add CORS headers to actual responses
def _build_cors_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "https://theologiananswers.com")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
