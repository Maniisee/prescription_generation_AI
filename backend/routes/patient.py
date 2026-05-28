"""
Patient Routes
Handles patient data management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db_manager import DatabaseManager

bp = Blueprint('patient', __name__)
db = DatabaseManager()

@bp.route('/create', methods=['POST'])
@jwt_required()
def create_patient():
    """
    Create or update patient record
    Request body: {
        patient_name (required), patient_id_number, date_of_birth,
        age (required), gender (required), phone, email, address,
        blood_pressure_systolic, blood_pressure_diastolic,
        temperature, pulse, weight, height, symptoms, medical_history,
        emergency_contact_name, emergency_contact_phone
    }
    """
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_name', 'age', 'gender']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'status': 'error', 
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Extract patient details
        patient_data = {
            'user_id': user_id,
            'patient_name': data.get('patient_name'),
            'patient_id_number': data.get('patient_id_number'),
            'date_of_birth': data.get('date_of_birth'),
            'age': data.get('age'),
            'gender': data.get('gender'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'address': data.get('address'),
            'blood_pressure_systolic': data.get('blood_pressure_systolic'),
            'blood_pressure_diastolic': data.get('blood_pressure_diastolic'),
            'temperature': data.get('temperature'),
            'pulse': data.get('pulse'),
            'weight': data.get('weight'),
            'height': data.get('height'),
            'symptoms': data.get('symptoms', ''),
            'medical_history': data.get('medical_history', ''),
            'emergency_contact_name': data.get('emergency_contact_name'),
            'emergency_contact_phone': data.get('emergency_contact_phone')
        }
        
        # Save patient data
        patient_id = db.create_patient(patient_data)
        
        if patient_id:
            return jsonify({
                'status': 'success',
                'message': 'Patient record created',
                'patient_id': patient_id
            }), 201
        else:
            return jsonify({'status': 'error', 'message': 'Failed to create patient record'}), 500
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/get/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    """Get patient details by ID"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        patient = db.get_patient(patient_id, user_id)
        
        if patient:
            return jsonify({
                'status': 'success',
                'patient': patient
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Patient not found'}), 404
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/history', methods=['GET'])
@jwt_required()
def get_patient_history():
    """Get all patient records for current user"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        patients = db.get_user_patients(user_id)
        
        return jsonify({
            'status': 'success',
            'patients': patients
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@bp.route('/<int:patient_id>/complete-history', methods=['GET'])
@jwt_required()
def get_complete_patient_history(patient_id):
    """Get complete medical history with diagnoses and prescriptions"""
    try:
        user_id = int(get_jwt_identity())
        
        # Verify ownership
        patient = db.get_patient(patient_id, user_id)
        if not patient:
            return jsonify({
                'status': 'error',
                'message': 'Patient not found or unauthorized'
            }), 404
        
        conn = db.connect()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Database connection failed'
            }), 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    d.id as diagnosis_id,
                    d.disease,
                    d.confidence,
                    d.symptoms,
                    d.vitals,
                    d.created_at as diagnosis_date,
                    pr.id as prescription_id,
                    pr.medications,
                    pr.instructions,
                    pr.precautions,
                    pr.created_at as prescription_date
                FROM diagnoses d
                LEFT JOIN prescriptions pr ON d.id = pr.diagnosis_id
                WHERE d.patient_id = %s
                ORDER BY d.created_at DESC
            """
            cursor.execute(query, (patient_id,))
            history = cursor.fetchall()
            cursor.close()
            
            return jsonify({
                'status': 'success',
                'patient': patient,
                'history': history
            }), 200
        
        finally:
            db.close()
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
