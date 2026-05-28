"""
Database Manager
Handles all MySQL database operations
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'disease_detection')
        self.connection = None
    
    def connect(self):
        """Create database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    # User operations
    def user_exists(self, email):
        """Check if user exists by email"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Error as e:
            print(f"Error checking user: {e}")
            return False
        finally:
            self.close()
    
    def create_user(self, email, hashed_password, name, phone=''):
        """Create new user"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO users (email, password, name, phone)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (email, hashed_password.decode('utf-8'), name, phone))
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return user_id
        except Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            self.close()
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            self.close()
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, email, name, phone FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            self.close()
    
    # Patient operations
    def create_patient(self, patient_data):
        """Create or update patient record with full patient identification"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO patients 
                (user_id, patient_name, patient_id_number, date_of_birth, age, gender, 
                 phone, email, address, blood_pressure_systolic, blood_pressure_diastolic,
                 temperature, pulse, weight, height, symptoms, medical_history,
                 emergency_contact_name, emergency_contact_phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                patient_data['user_id'],
                patient_data.get('patient_name'),
                patient_data.get('patient_id_number'),
                patient_data.get('date_of_birth'),
                patient_data['age'],
                patient_data['gender'],
                patient_data.get('phone'),
                patient_data.get('email'),
                patient_data.get('address'),
                patient_data.get('blood_pressure_systolic'),
                patient_data.get('blood_pressure_diastolic'),
                patient_data.get('temperature'),
                patient_data.get('pulse'),
                patient_data.get('weight'),
                patient_data.get('height'),
                patient_data.get('symptoms', ''),
                patient_data.get('medical_history', ''),
                patient_data.get('emergency_contact_name'),
                patient_data.get('emergency_contact_phone')
            )
            cursor.execute(query, values)
            conn.commit()
            patient_id = cursor.lastrowid
            cursor.close()
            return patient_id
        except Error as e:
            print(f"Error creating patient: {e}")
            return None
        finally:
            self.close()
    
    def get_patient(self, patient_id, user_id):
        """Get patient by ID and verify ownership"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM patients WHERE id = %s AND user_id = %s"
            cursor.execute(query, (patient_id, user_id))
            patient = cursor.fetchone()
            cursor.close()
            return patient
        except Error as e:
            print(f"Error getting patient: {e}")
            return None
        finally:
            self.close()
    
    def get_user_patients(self, user_id):
        """Get all patients for a user"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = cursor.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
            patients = cursor.fetchall()
            cursor.close()
            return patients
        except Error as e:
            print(f"Error getting patients: {e}")
            return []
        finally:
            self.close()
    
    # Diagnosis operations
    def save_diagnosis(self, patient_id, disease, confidence, symptoms, vitals):
        """Save diagnosis result"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO diagnoses (patient_id, disease, confidence, symptoms, vitals)
                VALUES (%s, %s, %s, %s, %s)
            """
            import json
            cursor.execute(query, (
                patient_id,
                disease,
                confidence,
                json.dumps(symptoms),
                json.dumps(vitals)
            ))
            conn.commit()
            diagnosis_id = cursor.lastrowid
            cursor.close()
            return diagnosis_id
        except Error as e:
            print(f"Error saving diagnosis: {e}")
            return None
        finally:
            self.close()
    
    def get_diagnosis(self, diagnosis_id):
        """Get diagnosis by ID"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM diagnoses WHERE id = %s", (diagnosis_id,))
            diagnosis = cursor.fetchone()
            cursor.close()
            
            if diagnosis:
                import json
                diagnosis['symptoms'] = json.loads(diagnosis['symptoms'])
                diagnosis['vitals'] = json.loads(diagnosis['vitals'])
            
            return diagnosis
        except Error as e:
            print(f"Error getting diagnosis: {e}")
            return None
        finally:
            self.close()
    
    def get_patient_diagnoses(self, patient_id):
        """Get all diagnoses for a patient"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM diagnoses WHERE patient_id = %s ORDER BY created_at DESC",
                (patient_id,)
            )
            diagnoses = cursor.fetchall()
            cursor.close()
            
            import json
            for d in diagnoses:
                d['symptoms'] = json.loads(d['symptoms'])
                d['vitals'] = json.loads(d['vitals'])
            
            return diagnoses
        except Error as e:
            print(f"Error getting diagnoses: {e}")
            return []
        finally:
            self.close()
    
    # Prescription operations
    def save_prescription(self, diagnosis_id, medications, dosage, instructions, precautions):
        """Save prescription"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO prescriptions (diagnosis_id, medications, dosage, instructions, precautions)
                VALUES (%s, %s, %s, %s, %s)
            """
            import json
            cursor.execute(query, (
                diagnosis_id,
                json.dumps(medications),
                dosage,
                instructions,
                precautions
            ))
            conn.commit()
            prescription_id = cursor.lastrowid
            cursor.close()
            return prescription_id
        except Error as e:
            print(f"Error saving prescription: {e}")
            return None
        finally:
            self.close()
    
    def get_prescription(self, prescription_id):
        """Get prescription by ID"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM prescriptions WHERE id = %s", (prescription_id,))
            prescription = cursor.fetchone()
            cursor.close()
            
            if prescription:
                import json
                prescription['medications'] = json.loads(prescription['medications'])
            
            return prescription
        except Error as e:
            print(f"Error getting prescription: {e}")
            return None
        finally:
            self.close()
    
    def get_patient_prescriptions(self, patient_id):
        """Get all prescriptions for a patient"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.* FROM prescriptions p
                JOIN diagnoses d ON p.diagnosis_id = d.id
                WHERE d.patient_id = %s
                ORDER BY p.created_at DESC
            """
            cursor.execute(query, (patient_id,))
            prescriptions = cursor.fetchall()
            cursor.close()
            
            import json
            for p in prescriptions:
                p['medications'] = json.loads(p['medications'])
            
            return prescriptions
        except Error as e:
            print(f"Error getting prescriptions: {e}")
            return []
        finally:
            self.close()
