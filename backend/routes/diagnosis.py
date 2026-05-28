"""
Diagnosis Routes
Handles disease prediction using AI/ML models
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.disease_classifier import DiseaseClassifier
from database.db_manager import DatabaseManager

bp = Blueprint('diagnosis', __name__)
db = DatabaseManager()
classifier = DiseaseClassifier()

@bp.route('/predict', methods=['POST'])
@jwt_required()
def predict_disease():
    """
    Predict disease based on symptoms and vitals
    Request body: {
        patient_id, symptoms (list), vitals (dict)
    }
    """
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        data = request.get_json()
        
        patient_id = data.get('patient_id')
        symptoms = data.get('symptoms', [])
        vitals = data.get('vitals', {})
        
        if not patient_id or not symptoms:
            return jsonify({'status': 'error', 'message': 'Missing required data'}), 400
        
        # Get patient data
        patient = db.get_patient(patient_id, user_id)
        if not patient:
            return jsonify({'status': 'error', 'message': 'Patient not found'}), 404
        
        # Predict disease
        prediction = classifier.predict(symptoms, vitals, patient)
        
        if prediction:
            # Save diagnosis
            diagnosis_id = db.save_diagnosis(
                patient_id=patient_id,
                disease=prediction['disease'],
                confidence=prediction['confidence'],
                symptoms=symptoms,
                vitals=vitals
            )
            
            return jsonify({
                'status': 'success',
                'diagnosis_id': diagnosis_id,
                'patient_id': patient_id,
                'prediction': prediction
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Prediction failed'}), 500
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/history/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_diagnosis_history(patient_id):
    """Get diagnosis history for a patient"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        
        # Verify patient belongs to user
        patient = db.get_patient(patient_id, user_id)
        if not patient:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
        diagnoses = db.get_patient_diagnoses(patient_id)
        
        return jsonify({
            'status': 'success',
            'diagnoses': diagnoses
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
