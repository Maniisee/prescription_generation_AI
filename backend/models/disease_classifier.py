"""
Disease Classifier - ML Model for Disease Prediction
Uses Random Forest and symptom matching
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import os

class DiseaseClassifier:
    def __init__(self):
        self.model = None
        self.mlb = None
        self.disease_symptoms = self.load_disease_database()
        self.model_path = os.path.join(os.path.dirname(__file__), 'disease_model.pkl')
        self.load_model()
    
    def load_disease_database(self):
        """Load disease-symptom mapping"""
        return {
            'Common Cold': [
                'runny nose', 'sore throat', 'cough', 'sneezing',
                'nasal congestion', 'mild headache', 'fatigue'
            ],
            'Flu': [
                'fever', 'body aches', 'fatigue', 'cough',
                'headache', 'chills', 'sore throat', 'muscle pain'
            ],
            'Diabetes': [
                'increased thirst', 'frequent urination', 'fatigue',
                'blurred vision', 'slow healing', 'tingling hands', 'weight loss'
            ],
            'Hypertension': [
                'headache', 'dizziness', 'chest pain', 'shortness of breath',
                'nosebleeds', 'vision problems'
            ],
            'Asthma': [
                'shortness of breath', 'wheezing', 'coughing',
                'chest tightness', 'difficulty breathing'
            ],
            'Migraine': [
                'intense headache', 'nausea', 'light sensitivity',
                'sound sensitivity', 'visual disturbances', 'vomiting'
            ],
            'Gastritis': [
                'stomach pain', 'nausea', 'bloating', 'indigestion',
                'loss of appetite', 'vomiting', 'burning sensation'
            ],
            'Pneumonia': [
                'chest pain', 'cough with phlegm', 'fever',
                'difficulty breathing', 'fatigue', 'confusion', 'sweating'
            ],
            'Allergic Rhinitis': [
                'sneezing', 'itchy nose', 'congestion', 'watery eyes',
                'runny nose', 'postnasal drip'
            ],
            'Bronchitis': [
                'cough', 'mucus production', 'fatigue', 'chest discomfort',
                'shortness of breath', 'slight fever'
            ]
        }
    
    def load_model(self):
        """Load pre-trained model if exists"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print("Model loaded successfully")
            except:
                print("Model file found but failed to load, using rule-based fallback")
                self.model = None
        else:
            print("No pre-trained model found, using rule-based prediction")
            self.model = None
    
    def preprocess_symptoms(self, symptoms):
        """Normalize symptom text"""
        processed = []
        for symptom in symptoms:
            symptom_lower = symptom.lower().strip()
            processed.append(symptom_lower)
        return processed
    
    def calculate_symptom_match(self, patient_symptoms, disease_symptoms):
        """Calculate match percentage between symptoms"""
        patient_set = set(self.preprocess_symptoms(patient_symptoms))
        disease_set = set(disease_symptoms)
        
        matches = len(patient_set.intersection(disease_set))
        total = len(patient_set)
        
        if total == 0:
            return 0
        
        return (matches / total) * 100
    
    def check_vitals_risk(self, vitals):
        """Check if vitals indicate specific conditions"""
        risks = []
        
        # Blood pressure check
        bp_sys = vitals.get('blood_pressure_systolic', 0)
        bp_dia = vitals.get('blood_pressure_diastolic', 0)
        
        if bp_sys >= 140 or bp_dia >= 90:
            risks.append(('Hypertension', 80))
        elif bp_sys >= 130 or bp_dia >= 80:
            risks.append(('Hypertension', 60))
        
        # Temperature check
        temp = vitals.get('temperature', 0)
        if temp >= 100.4:  # Fahrenheit
            risks.append(('Fever-related', 70))
        
        # Pulse check
        pulse = vitals.get('pulse', 0)
        if pulse > 100:
            risks.append(('Tachycardia', 60))
        elif pulse < 60:
            risks.append(('Bradycardia', 60))
        
        return risks
    
    def predict(self, symptoms, vitals, patient_data):
        """
        Predict disease based on symptoms and vitals
        Returns: {disease, confidence, description, recommendations}
        """
        if not symptoms:
            return None
        
        # Preprocess symptoms
        patient_symptoms = self.preprocess_symptoms(symptoms)
        
        # Calculate match scores for all diseases
        scores = {}
        for disease, disease_symptoms in self.disease_symptoms.items():
            score = self.calculate_symptom_match(patient_symptoms, disease_symptoms)
            scores[disease] = score
        
        # Check vital signs
        vital_risks = self.check_vitals_risk(vitals)
        for disease, risk_score in vital_risks:
            if disease in scores:
                scores[disease] = min(100, scores[disease] + risk_score * 0.3)
        
        # Get top prediction
        if not scores:
            return None
        
        top_disease = max(scores, key=scores.get)
        confidence = scores[top_disease]
        
        # Get additional predictions
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        alternatives = [
            {'disease': d, 'confidence': round(c, 2)}
            for d, c in sorted_scores[1:4] if c > 20
        ]
        
        return {
            'disease': top_disease,
            'confidence': round(confidence, 2),
            'alternatives': alternatives,
            'matched_symptoms': self.get_matched_symptoms(patient_symptoms, top_disease),
            'description': self.get_disease_description(top_disease),
            'severity': self.get_disease_severity(top_disease),
            'recommendations': self.get_recommendations(top_disease, confidence)
        }
    
    def get_matched_symptoms(self, patient_symptoms, disease):
        """Get list of matched symptoms"""
        disease_symptoms = set(self.disease_symptoms.get(disease, []))
        matched = [s for s in patient_symptoms if s in disease_symptoms]
        return matched
    
    def get_disease_description(self, disease):
        """Get disease description"""
        descriptions = {
            'Common Cold': 'Viral infection of the upper respiratory tract',
            'Flu': 'Influenza viral infection causing respiratory and systemic symptoms',
            'Diabetes': 'Metabolic disorder characterized by high blood sugar levels',
            'Hypertension': 'Elevated blood pressure that can lead to serious complications',
            'Asthma': 'Chronic respiratory condition causing airway inflammation',
            'Migraine': 'Neurological condition causing severe headaches',
            'Gastritis': 'Inflammation of the stomach lining',
            'Pneumonia': 'Infection causing inflammation of lung air sacs',
            'Allergic Rhinitis': 'Allergic response causing nasal inflammation',
            'Bronchitis': 'Inflammation of bronchial tubes carrying air to lungs'
        }
        return descriptions.get(disease, 'Medical condition requiring evaluation')
    
    def get_disease_severity(self, disease):
        """Get disease severity level"""
        severity_map = {
            'Common Cold': 'low',
            'Flu': 'medium',
            'Diabetes': 'high',
            'Hypertension': 'high',
            'Asthma': 'medium',
            'Migraine': 'medium',
            'Gastritis': 'medium',
            'Pneumonia': 'high',
            'Allergic Rhinitis': 'low',
            'Bronchitis': 'medium'
        }
        return severity_map.get(disease, 'medium')
    
    def get_recommendations(self, disease, confidence):
        """Get general recommendations"""
        if confidence < 50:
            return [
                'Symptoms are not conclusive',
                'Consider consulting a healthcare professional',
                'Monitor symptoms for changes',
                'Maintain detailed symptom diary'
            ]
        
        general = [
            'This is a preliminary AI-based assessment',
            'Consult a licensed healthcare professional for accurate diagnosis',
            'Follow prescribed treatment plan',
            'Monitor symptoms and report changes'
        ]
        
        return general
    
    def train_model(self, training_data):
        """Train ML model with labeled data (future enhancement)"""
        # This would be implemented when we have sufficient training data
        pass
