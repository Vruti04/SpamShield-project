from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import os
import re
from waitress import serve  # Production WSGI server

app = Flask(__name__, static_folder='.', template_folder='.')

# Security: CORS configuration
CORS(app)

# Load model and vectorizer
MODEL_PATH = "spam_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    model = None
    vectorizer = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def js():
    return send_from_directory('.', 'script.js')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": "Model not trained yet."}), 500
    
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    message = data.get("message", "")
    
    if len(message) > 5000:
        return jsonify({"error": "Message too long. Maximum 5000 characters."}), 400
    
    if not message.strip():
        return jsonify({"error": "Empty message"}), 400
    
    clean_message = re.sub(r'<[^>]*?>', '', message)
    
    try:
        vec = vectorizer.transform([clean_message])
        prediction = int(model.predict(vec)[0])
        probabilities = model.predict_proba(vec)[0]
        confidence = float(max(probabilities)) * 100
        
        return jsonify({
            "is_spam": prediction == 1,
            "confidence": confidence
        })
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://fonts.googleapis.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; connect-src 'self'"
    return response

if __name__ == '__main__':
    print("🚀 SpamShield Server starting on http://127.0.0.1:5000")
    # Using Waitress as the production-ready WSGI server
    serve(app, host='127.0.0.1', port=5000)
