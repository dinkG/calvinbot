from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)

# Allow CORS for specific origin with necessary headers and support for preflight requests
CORS(app, resources={r"/chat": {"origins": "https://theologiananswers.com"}}, supports_credentials=True)

# Configure the database URI (update this with your actual database credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/theologian_chatbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Define the User model to store user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    signup_date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Define the Interaction model to store user interactions with theologians
class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=False)
    theologian = db.Column(db.String(50), nullable=False)
    response = db.Column(db.Text, nullable=False)
    citation = db.Column(db.Text, nullable=True)  # Add citation field
    interaction_date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Define the API URLs for different theologians from environment variables or default URLs
API_URL_CALVIN = os.getenv('API_URL_CALVIN', 'https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/')
API_URL_AUGUSTINE = os.getenv('API_URL_AUGUSTINE', 'https://augustine-api.com/dev/')
API_URL_AQUINAS = os.getenv('API_URL_AQUINAS', 'https://aquinas-api.com/dev/')
API_URL_LUTHER = os.getenv('API_URL_LUTHER', 'https://co9rp2odta.execute-api.us-east-1.amazonaws.com/Dev/')
API_URL_EDWARDS = os.getenv('API_URL_EDWARDS', 'https://edwards-api.com/dev/')

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return _build_cors_prelight_response()
    
    data = request.get_json()

    if 'question' not in data or 'theologian' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_question = data['question']
    theologian = data['theologian']
    user_email = data['email']

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
            citation = result.get('Citation', '')  # Extract citation

            # Store the interaction in the database
            interaction = Interaction(user_email=user_email, question=user_question, theologian=theologian, response=answer, citation=citation)
            db.session.add(interaction)
            db.session.commit()

            return _build_cors_actual_response(jsonify({"answer": answer, "citation": citation}))  # Include citation in response
        else:
            return _build_cors_actual_response(jsonify({
                "error": "Error from API",
                "status_code": response.status_code,
                "response": response.text
            }), 500)

    except requests.exceptions.RequestException as e:
        return _build_cors_actual_response(jsonify({"error": "API request failed", "message": str(e)}), 500)

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
    db.create_all()  # This creates the tables if they don't already exist
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
