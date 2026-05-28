"""
Prescription Routes
Handles prescription generation and retrieval
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.ai_prescription_generator import LocalLLMPrescriptionGenerator
from database.db_manager import DatabaseManager

bp = Blueprint('prescription', __name__)
db = DatabaseManager()
# Using LLaMA 3 via Ollama for AI-powered prescriptions
# Falls back to rule-based if Ollama is not running
generator = LocalLLMPrescriptionGenerator(model_name="llama3")

@bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_prescription():
    """
    Generate prescription based on diagnosis
    Request body: {diagnosis_id}
    """
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        data = request.get_json()
        
        diagnosis_id = data.get('diagnosis_id')
        
        if not diagnosis_id:
            return jsonify({'status': 'error', 'message': 'Diagnosis ID required'}), 400
        
        # Get diagnosis
        diagnosis = db.get_diagnosis(diagnosis_id)
        if not diagnosis:
            return jsonify({'status': 'error', 'message': 'Diagnosis not found'}), 404
        
        # Verify ownership
        patient = db.get_patient(diagnosis['patient_id'], user_id)
        if not patient:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
        # Generate prescription
        prescription = generator.generate(diagnosis, patient)
        
        if prescription:
            # Convert lists to strings for database storage
            instructions_text = '\n'.join(prescription['instructions']) if isinstance(prescription['instructions'], list) else prescription['instructions']
            precautions_text = '\n'.join(prescription['precautions']) if isinstance(prescription['precautions'], list) else prescription['precautions']
            
            # Save prescription - dosage info is in medications, use empty string for dosage field
            prescription_id = db.save_prescription(
                diagnosis_id=diagnosis_id,
                medications=prescription['medications'],
                dosage='',  # Dosage is embedded in medications list
                instructions=instructions_text,
                precautions=precautions_text
            )
            
            return jsonify({
                'status': 'success',
                'prescription_id': prescription_id,
                'prescription': prescription
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Prescription generation failed'}), 500
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/get/<int:prescription_id>', methods=['GET'])
@jwt_required()
def get_prescription(prescription_id):
    """Get prescription by ID"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        
        prescription = db.get_prescription(prescription_id)
        if not prescription:
            return jsonify({'status': 'error', 'message': 'Prescription not found'}), 404
        
        # Verify ownership
        diagnosis = db.get_diagnosis(prescription['diagnosis_id'])
        patient = db.get_patient(diagnosis['patient_id'], user_id)
        if not patient:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
        return jsonify({
            'status': 'success',
            'prescription': prescription
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_prescriptions(patient_id):
    """Get all prescriptions for a patient"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        
        # Verify ownership
        patient = db.get_patient(patient_id, user_id)
        if not patient:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
        prescriptions = db.get_patient_prescriptions(patient_id)
        
        return jsonify({
            'status': 'success',
            'prescriptions': prescriptions
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
