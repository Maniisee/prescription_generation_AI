"""
Flask Application - AI Disease Detection & Prescription System
Main entry point for the backend API server
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import bcrypt
from datetime import timedelta
import os

# Load environment variables
load_dotenv()

# Import routes
from backend.routes import auth, patient, diagnosis, prescription

# Initialize Flask app
app = Flask(__name__)

# Configure CORS with explicit settings
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(patient.bp, url_prefix='/api/patient')
app.register_blueprint(diagnosis.bp, url_prefix='/api/diagnosis')
app.register_blueprint(prescription.bp, url_prefix='/api/prescription')

# Root route
@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'AI Disease Detection API is running',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'patient': '/api/patient',
            'diagnosis': '/api/diagnosis',
            'prescription': '/api/prescription'
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'status': 'error', 'message': 'Bad request'}), 400

# JWT error handlers
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({'status': 'error', 'message': 'Authorization required'}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({'status': 'error', 'message': 'Token has expired'}), 401

if __name__ == '__main__':
    # Run in debug mode for development
    # Using port 5001 since macOS AirPlay Receiver uses 5000
    # Using host='127.0.0.1' to explicitly bind to IPv4 only
    # (Browsers try IPv6 ::1 first with 'localhost', causing connection refused)
    port = int(os.getenv('FLASK_RUN_PORT', 5001))
    app.run(host='127.0.0.1', port=port, debug=False)
