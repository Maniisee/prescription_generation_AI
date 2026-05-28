"""
Authentication Routes
Handles user signup, login, and authentication
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
import re
from database.db_manager import DatabaseManager

bp = Blueprint('auth', __name__)
db = DatabaseManager()

@bp.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user
    Request body: {email, password, name, phone}
    """
    try:
        data = request.get_json()
        
        # Validate input
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        if not all([email, password, name]):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Validate email format
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
        
        # Check password strength
        if len(password) < 8:
            return jsonify({'status': 'error', 'message': 'Password must be at least 8 characters'}), 400
        
        # Check if user already exists
        if db.user_exists(email):
            return jsonify({'status': 'error', 'message': 'User already exists'}), 409
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        user_id = db.create_user(email, hashed_password, name, phone)
        
        if user_id:
            return jsonify({
                'status': 'success',
                'message': 'User registered successfully',
                'user_id': user_id
            }), 201
        else:
            return jsonify({'status': 'error', 'message': 'Registration failed'}), 500
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token
    Request body: {email, password}
    """
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not all([email, password]):
            return jsonify({'status': 'error', 'message': 'Missing email or password'}), 400
        
        # Get user from database
        user = db.get_user_by_email(email)
        
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Create JWT token with string identity
            access_token = create_access_token(identity=str(user['id']))
            
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'access_token': access_token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name']
                }
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/verify', methods=['GET'])
def verify_token():
    """
    Verify if JWT token is valid
    Requires: Authorization header with Bearer token
    """
    try:
        from flask_jwt_extended import jwt_required, get_jwt_identity
        
        @jwt_required()
        def verify():
            user_id = int(get_jwt_identity())  # Convert string to int
            user = db.get_user_by_id(user_id)
            
            if user:
                return jsonify({
                    'status': 'success',
                    'valid': True,
                    'user': {
                        'id': user['id'],
                        'email': user['email'],
                        'name': user['name']
                    }
                }), 200
            else:
                return jsonify({'status': 'error', 'valid': False}), 401
        
        return verify()
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
