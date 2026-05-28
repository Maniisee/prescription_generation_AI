"""
Disease Classification Model
Uses symptom matching and vital signs analysis to predict diseases
"""

import json
from typing import Dict, List, Tuple

class DiseaseClassifier:
    """
    AI model for disease classification based on symptoms and vital signs
    Uses rule-based matching with confidence scoring
    """
    
    def __init__(self):
        """Initialize the disease classifier with disease database"""
        self.diseases = self._load_disease_database()
    
    def _load_disease_database(self) -> Dict:
        """Load disease information with symptoms"""
        return {
            'Common Cold': {
                'symptoms': ['runny nose', 'sneezing', 'sore throat', 'cough', 'mild fever', 'nasal congestion', 'headache', 'fatigue'],
                'severity': 'low',
                'description': 'Viral infection of the upper respiratory tract'
            },
            'Flu': {
                'symptoms': ['high fever', 'body aches', 'fatigue', 'headache', 'dry cough', 'chills', 'sweating', 'sore throat'],
                'severity': 'medium',
                'description': 'Influenza viral infection affecting the respiratory system'
            },
            'Diabetes': {
                'symptoms': ['increased thirst', 'frequent urination', 'fatigue', 'blurred vision', 'weight loss', 'slow wound healing'],
                'severity': 'high',
                'description': 'Metabolic disorder characterized by high blood sugar levels'
            },
            'Hypertension': {
                'symptoms': ['headache', 'dizziness', 'chest pain', 'shortness of breath', 'fatigue', 'irregular heartbeat'],
                'severity': 'high',
                'description': 'Chronic elevation of blood pressure'
            },
            'Asthma': {
                'symptoms': ['shortness of breath', 'wheezing', 'chest tightness', 'coughing', 'difficulty breathing'],
                'severity': 'medium',
                'description': 'Chronic respiratory condition causing airway inflammation'
            },
            'Migraine': {
                'symptoms': ['severe headache', 'nausea', 'vomiting', 'sensitivity to light', 'visual disturbances', 'dizziness'],
                'severity': 'medium',
                'description': 'Neurological condition causing intense headaches'
            },
            'Gastritis': {
                'symptoms': ['stomach pain', 'nausea', 'vomiting', 'bloating', 'loss of appetite', 'indigestion'],
                'severity': 'medium',
                'description': 'Inflammation of the stomach lining'
            },
            'Pneumonia': {
                'symptoms': ['high fever', 'cough with mucus', 'chest pain', 'shortness of breath', 'fatigue', 'chills', 'rapid breathing'],
                'severity': 'high',
                'description': 'Infection of the lungs causing inflammation'
            },
            'Allergic Rhinitis': {
                'symptoms': ['sneezing', 'runny nose', 'itchy nose', 'watery eyes', 'nasal congestion', 'cough'],
                'severity': 'low',
                'description': 'Allergic reaction affecting the nasal passages'
            },
            'Bronchitis': {
                'symptoms': ['persistent cough', 'mucus production', 'chest discomfort', 'fatigue', 'shortness of breath', 'mild fever'],
                'severity': 'medium',
                'description': 'Inflammation of the bronchial tubes'
            }
        }
    
    def predict(self, symptoms: List[str], vitals: Dict, patient_data: Dict = None) -> Dict:
        """
        Predict disease based on symptoms and vital signs
        
        Args:
            symptoms: List of patient symptoms (strings)
            vitals: Dictionary with blood_pressure_systolic, blood_pressure_diastolic, temperature, pulse
            patient_data: Additional patient information (age, gender, medical_history)
        
        Returns:
            Dictionary with disease, confidence, alternatives, matched_symptoms, severity, recommendations
        """
        # Normalize symptoms
        symptoms_lower = [s.lower().strip() for s in symptoms]
        
        # Calculate matches for each disease
        disease_scores = []
        
        for disease_name, disease_info in self.diseases.items():
            disease_symptoms = [s.lower() for s in disease_info['symptoms']]
            
            # Calculate symptom match percentage
            matched = self._calculate_symptom_match(symptoms_lower, disease_symptoms)
            
            # Calculate vital signs risk factor
            vital_risk = self._check_vitals_risk(disease_name, vitals)
            
            # Combined confidence score
            confidence = (matched['percentage'] * 0.7) + (vital_risk * 0.3)
            
            disease_scores.append({
                'disease': disease_name,
                'confidence': confidence,
                'matched_symptoms': matched['matched'],
                'severity': disease_info['severity'],
                'description': disease_info['description']
            })
        
        # Sort by confidence
        disease_scores.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Get top prediction
        top_prediction = disease_scores[0]
        
        # Get alternatives (top 3 after main prediction)
        alternatives = [
            {'disease': d['disease'], 'confidence': d['confidence']}
            for d in disease_scores[1:4]
        ]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            top_prediction,
            vitals,
            patient_data
        )
        
        return {
            'disease': top_prediction['disease'],
            'confidence': top_prediction['confidence'],
            'matched_symptoms': top_prediction['matched_symptoms'],
            'severity': top_prediction['severity'],
            'description': top_prediction['description'],
            'alternatives': alternatives,
            'recommendations': recommendations
        }
    
    def _calculate_symptom_match(self, patient_symptoms: List[str], disease_symptoms: List[str]) -> Dict:
        """Calculate how well patient symptoms match disease symptoms"""
        matched_symptoms = []
        
        for p_symptom in patient_symptoms:
            for d_symptom in disease_symptoms:
                # Check for exact match or partial match
                if p_symptom in d_symptom or d_symptom in p_symptom:
                    matched_symptoms.append(p_symptom)
                    break
        
        # Calculate match percentage
        if len(disease_symptoms) > 0:
            percentage = (len(matched_symptoms) / len(disease_symptoms)) * 100
        else:
            percentage = 0
        
        return {
            'matched': matched_symptoms,
            'percentage': percentage
        }
    
    def _check_vitals_risk(self, disease_name: str, vitals: Dict) -> float:
        """Check if vital signs indicate risk for specific disease"""
        risk_score = 0.0
        
        # Extract vitals (handle None values)
        bp_sys = vitals.get('blood_pressure_systolic')
        bp_dia = vitals.get('blood_pressure_diastolic')
        temp = vitals.get('temperature')
        pulse = vitals.get('pulse')
        
        # Hypertension check
        if disease_name == 'Hypertension':
            if bp_sys and bp_sys > 140:
                risk_score += 40
            if bp_dia and bp_dia > 90:
                risk_score += 30
        
        # Fever-related diseases
        if disease_name in ['Flu', 'Pneumonia', 'Bronchitis', 'Common Cold']:
            if temp and temp > 100.4:
                risk_score += 50
        
        # Heart-related checks
        if disease_name in ['Hypertension', 'Asthma']:
            if pulse and (pulse > 100 or pulse < 60):
                risk_score += 30
        
        return min(risk_score, 100)
    
    def _generate_recommendations(self, prediction: Dict, vitals: Dict, patient_data: Dict = None) -> List[str]:
        """Generate health recommendations based on prediction"""
        recommendations = []
        
        confidence = prediction['confidence']
        severity = prediction['severity']
        
        # Confidence-based recommendations
        if confidence < 70:
            recommendations.append("Low confidence - Strongly recommend consulting a doctor for accurate diagnosis")
        
        # Severity-based recommendations
        if severity in ['high', 'critical']:
            recommendations.append("High severity condition - Seek immediate medical attention")
        
        # Vital signs recommendations
        bp_sys = vitals.get('blood_pressure_systolic')
        if bp_sys and bp_sys > 140:
            recommendations.append("Blood pressure is elevated - Monitor regularly and consult a doctor")
        
        temp = vitals.get('temperature')
        if temp and temp > 102:
            recommendations.append("High fever detected - Stay hydrated and consider fever-reducing medication")
        
        # Age-based recommendations
        if patient_data:
            age = patient_data.get('age', 0)
            if age > 65 or age < 18:
                recommendations.append("Special care needed - Consult with appropriate specialist")
        
        return recommendations
    
    def train(self, training_data: List[Dict]):
        """
        Train the model with new data
        (Placeholder for future machine learning implementation)
        """
        # TODO: Implement ML training when dataset is available
        pass
    
    def save_model(self, filepath: str):
        """Save model to file"""
        import joblib
        joblib.dump(self.diseases, filepath)
    
    def load_model(self, filepath: str):
        """Load model from file"""
        import joblib
        self.diseases = joblib.load(filepath)
