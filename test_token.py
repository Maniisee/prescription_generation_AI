import sys
import json
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, decode_token

# Add the project to path
sys.path.insert(0, '/Users/manikandank/Downloads/disease_detection_ai')

# Test JWT token creation and decoding
from backend.app import app

with app.app_context():
    # Create a test token
    token = create_access_token(identity=1)
    print(f"Generated token: {token}")
    print(f"\nToken length: {len(token)}")
    
    # Try to decode it
    try:
        decoded = decode_token(token)
        print(f"\nDecoded successfully:")
        print(json.dumps(decoded, indent=2, default=str))
    except Exception as e:
        print(f"\nError decoding: {e}")
