"""
Prescription Generation Module
Generates treatment recommendations based on disease diagnosis
"""

from typing import Dict, List

class PrescriptionGenerator:
    """
    Generates prescriptions with medications, dosage, and instructions
    based on the diagnosed disease
    """
    
    def __init__(self):
        """Initialize prescription generator with treatment database"""
        self.treatments = self._load_treatment_database()
    
    def _load_treatment_database(self) -> Dict:
        """Load treatment protocols for different diseases"""
        return {
            'Common Cold': {
                'medications': [
                    {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'Every 6 hours', 'duration': '3-5 days'},
                    {'name': 'Antihistamine (Cetirizine)', 'dosage': '10mg', 'frequency': 'Once daily', 'duration': '5 days'}
                ],
                'instructions': [
                    'Get plenty of rest',
                    'Drink warm fluids (tea, soup)',
                    'Use saline nasal drops',
                    'Gargle with warm salt water',
                    'Avoid cold drinks and ice cream'
                ],
                'precautions': [
                    'Avoid contact with others to prevent spread',
                    'Cover mouth when coughing or sneezing',
                    'Wash hands frequently',
                    'Consult doctor if symptoms worsen after 7 days'
                ]
            },
            'Flu': {
                'medications': [
                    {'name': 'Oseltamivir (Tamiflu)', 'dosage': '75mg', 'frequency': 'Twice daily', 'duration': '5 days'},
                    {'name': 'Paracetamol', 'dosage': '650mg', 'frequency': 'Every 6 hours', 'duration': '5-7 days'},
                    {'name': 'Cough Syrup', 'dosage': '10ml', 'frequency': 'Three times daily', 'duration': '5 days'}
                ],
                'instructions': [
                    'Complete bed rest recommended',
                    'Stay well hydrated',
                    'Take medications with food',
                    'Monitor temperature regularly',
                    'Isolate to prevent spread'
                ],
                'precautions': [
                    'Seek immediate care if breathing difficulty develops',
                    'Watch for signs of dehydration',
                    'Avoid aspirin if under 18 years',
                    'Return to doctor if fever persists beyond 3 days'
                ]
            },
            'Diabetes': {
                'medications': [
                    {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily with meals', 'duration': 'Long-term'},
                    {'name': 'Glimepiride', 'dosage': '1mg', 'frequency': 'Once daily before breakfast', 'duration': 'Long-term'}
                ],
                'instructions': [
                    'Monitor blood sugar levels daily',
                    'Follow diabetic diet plan',
                    'Regular exercise (30 min daily)',
                    'Avoid sugary foods and drinks',
                    'Eat small frequent meals',
                    'Check HbA1c levels every 3 months'
                ],
                'precautions': [
                    'Watch for signs of hypoglycemia (low blood sugar)',
                    'Keep glucose tablets or candy available',
                    'Regular eye and foot examinations',
                    'Inform doctor about any infections',
                    'Maintain healthy weight'
                ]
            },
            'Hypertension': {
                'medications': [
                    {'name': 'Amlodipine', 'dosage': '5mg', 'frequency': 'Once daily', 'duration': 'Long-term'},
                    {'name': 'Enalapril', 'dosage': '5mg', 'frequency': 'Once daily', 'duration': 'Long-term'}
                ],
                'instructions': [
                    'Monitor blood pressure daily',
                    'Reduce salt intake (less than 5g/day)',
                    'Regular physical activity',
                    'Maintain healthy weight',
                    'Limit alcohol consumption',
                    'Practice stress management'
                ],
                'precautions': [
                    'Do not stop medications suddenly',
                    'Report dizziness or fainting',
                    'Avoid high-sodium foods',
                    'Regular check-ups every 3 months',
                    'Watch for chest pain or irregular heartbeat'
                ]
            },
            'Asthma': {
                'medications': [
                    {'name': 'Salbutamol Inhaler', 'dosage': '100mcg', 'frequency': 'As needed (max 4 times/day)', 'duration': 'Long-term'},
                    {'name': 'Budesonide Inhaler', 'dosage': '200mcg', 'frequency': 'Twice daily', 'duration': 'Long-term'},
                    {'name': 'Montelukast', 'dosage': '10mg', 'frequency': 'Once daily at bedtime', 'duration': 'Long-term'}
                ],
                'instructions': [
                    'Always carry rescue inhaler',
                    'Avoid triggers (dust, smoke, pollen)',
                    'Use spacer device with inhaler',
                    'Monitor peak flow readings',
                    'Practice breathing exercises'
                ],
                'precautions': [
                    'Seek emergency care for severe breathing difficulty',
                    'Rinse mouth after using steroid inhaler',
                    'Keep environment dust-free',
                    'Get flu and pneumonia vaccines',
                    'Avoid cold air exposure'
                ]
            },
            'Migraine': {
                'medications': [
                    {'name': 'Sumatriptan', 'dosage': '50mg', 'frequency': 'At onset of headache', 'duration': 'As needed'},
                    {'name': 'Naproxen', 'dosage': '500mg', 'frequency': 'Twice daily', 'duration': 'During attack'},
                    {'name': 'Propranolol', 'dosage': '40mg', 'frequency': 'Once daily (preventive)', 'duration': 'Long-term'}
                ],
                'instructions': [
                    'Rest in dark, quiet room during attack',
                    'Apply cold compress to forehead',
                    'Identify and avoid triggers',
                    'Maintain regular sleep schedule',
                    'Stay hydrated',
                    'Keep a headache diary'
                ],
                'precautions': [
                    'Avoid excessive caffeine',
                    'Manage stress levels',
                    'Do not overuse pain medications',
                    'Seek care if headache pattern changes',
                    'Watch for aura symptoms'
                ]
            },
            'Gastritis': {
                'medications': [
                    {'name': 'Omeprazole', 'dosage': '20mg', 'frequency': 'Once daily before breakfast', 'duration': '4-8 weeks'},
                    {'name': 'Ranitidine', 'dosage': '150mg', 'frequency': 'Twice daily', 'duration': '4 weeks'},
                    {'name': 'Antacid Syrup', 'dosage': '10ml', 'frequency': 'After meals', 'duration': '2 weeks'}
                ],
                'instructions': [
                    'Eat smaller, more frequent meals',
                    'Avoid spicy and fried foods',
                    'Avoid alcohol and smoking',
                    'Do not lie down immediately after eating',
                    'Reduce stress levels',
                    'Avoid NSAIDs (aspirin, ibuprofen)'
                ],
                'precautions': [
                    'Watch for black stools or blood in vomit',
                    'Report severe abdominal pain',
                    'Complete medication course',
                    'Avoid late night eating',
                    'Test for H. pylori if recurrent'
                ]
            },
            'Pneumonia': {
                'medications': [
                    {'name': 'Amoxicillin', 'dosage': '500mg', 'frequency': 'Three times daily', 'duration': '7-10 days'},
                    {'name': 'Azithromycin', 'dosage': '500mg', 'frequency': 'Once daily', 'duration': '5 days'},
                    {'name': 'Paracetamol', 'dosage': '650mg', 'frequency': 'Every 6 hours', 'duration': '5-7 days'}
                ],
                'instructions': [
                    'Complete full course of antibiotics',
                    'Get plenty of rest',
                    'Drink lots of fluids',
                    'Use humidifier in room',
                    'Practice deep breathing exercises',
                    'Monitor oxygen levels if available'
                ],
                'precautions': [
                    'Seek emergency care if breathing severely difficult',
                    'Watch for bluish lips or fingernails',
                    'Complete antibiotic course even if feeling better',
                    'Follow up with chest X-ray',
                    'Avoid smoking and secondhand smoke'
                ]
            },
            'Allergic Rhinitis': {
                'medications': [
                    {'name': 'Cetirizine', 'dosage': '10mg', 'frequency': 'Once daily', 'duration': '2-4 weeks'},
                    {'name': 'Fluticasone Nasal Spray', 'dosage': '50mcg', 'frequency': 'Two sprays each nostril once daily', 'duration': '2-4 weeks'},
                    {'name': 'Pseudoephedrine', 'dosage': '60mg', 'frequency': 'As needed', 'duration': 'Short-term'}
                ],
                'instructions': [
                    'Avoid known allergens',
                    'Keep windows closed during high pollen season',
                    'Use air purifier',
                    'Wash bedding in hot water weekly',
                    'Shower before bed to remove pollen',
                    'Use saline nasal rinse'
                ],
                'precautions': [
                    'Avoid sedating antihistamines when driving',
                    'Do not use nasal spray for more than 3 days without doctor advice',
                    'Watch for signs of sinus infection',
                    'Consider allergy testing',
                    'Keep indoor humidity between 30-50%'
                ]
            },
            'Bronchitis': {
                'medications': [
                    {'name': 'Ambroxol', 'dosage': '30mg', 'frequency': 'Three times daily', 'duration': '5-7 days'},
                    {'name': 'Salbutamol', 'dosage': '4mg', 'frequency': 'Three times daily', 'duration': '5 days'},
                    {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'Every 6 hours', 'duration': '5 days'}
                ],
                'instructions': [
                    'Get plenty of rest',
                    'Drink warm fluids',
                    'Use humidifier or steam inhalation',
                    'Avoid smoking and smoke exposure',
                    'Practice controlled coughing',
                    'Avoid cold air'
                ],
                'precautions': [
                    'Watch for high fever or breathing difficulty',
                    'Do not suppress productive cough',
                    'Consult doctor if symptoms persist beyond 3 weeks',
                    'Avoid irritants like dust and fumes',
                    'Stay away from people who are sick'
                ]
            }
        }
    
    def generate(self, diagnosis: Dict, patient: Dict = None) -> Dict:
        """
        Generate prescription based on diagnosis
        
        Args:
            diagnosis: Dictionary with disease, confidence, severity
            patient: Patient information (age, gender, medical_history)
        
        Returns:
            Dictionary with medications, instructions, precautions, disclaimer
        """
        disease = diagnosis.get('disease', '')
        confidence = diagnosis.get('confidence', 0)
        
        # Get treatment for disease
        if disease not in self.treatments:
            return self._generate_generic_prescription()
        
        treatment = self.treatments[disease]
        
        # Base prescription
        prescription = {
            'medications': treatment['medications'],
            'instructions': treatment['instructions'],
            'precautions': treatment['precautions'],
            'disclaimer': self._generate_disclaimer(confidence)
        }
        
        # Customize based on patient data
        if patient:
            prescription = self._customize_prescription(prescription, patient, diagnosis)
        
        return prescription
    
    def _customize_prescription(self, prescription: Dict, patient: Dict, diagnosis: Dict) -> Dict:
        """Customize prescription based on patient details"""
        age = patient.get('age', 30)
        medical_history = patient.get('medical_history', '')
        
        # Age-based modifications
        if age < 18:
            prescription['precautions'].append('Pediatric case - Consult pediatrician for dose adjustment')
        elif age > 65:
            prescription['precautions'].append('Elderly patient - Monitor for drug interactions and side effects')
        
        # Confidence-based additions
        if diagnosis.get('confidence', 0) < 70:
            prescription['precautions'].insert(0, 'LOW CONFIDENCE DIAGNOSIS - Strongly recommend consulting a doctor')
        
        # Vital signs warnings
        vitals = diagnosis.get('vitals', {})
        if vitals.get('temperature') and vitals['temperature'] > 102:
            prescription['precautions'].insert(0, 'HIGH FEVER - Seek immediate medical attention if fever persists')
        
        if vitals.get('blood_pressure_systolic') and vitals['blood_pressure_systolic'] > 160:
            prescription['precautions'].insert(0, 'VERY HIGH BLOOD PRESSURE - Seek immediate medical attention')
        
        return prescription
    
    def _generate_generic_prescription(self) -> Dict:
        """Generate generic prescription for unknown diseases"""
        return {
            'medications': [
                {'name': 'Over-the-counter pain reliever', 'dosage': 'As directed', 'frequency': 'As needed', 'duration': 'Short-term'}
            ],
            'instructions': [
                'Rest and stay hydrated',
                'Monitor symptoms',
                'Maintain healthy diet',
                'Consult doctor if symptoms persist'
            ],
            'precautions': [
                'This is a preliminary assessment',
                'Please consult a qualified healthcare provider',
                'Seek emergency care if symptoms worsen'
            ],
            'disclaimer': 'This diagnosis could not be determined with confidence. Please consult a healthcare professional.'
        }
    
    def _generate_disclaimer(self, confidence: float) -> str:
        """Generate disclaimer based on confidence level"""
        if confidence >= 80:
            return ("This is an AI-generated prescription based on your symptoms. "
                   "While confidence is high, please consult a qualified healthcare provider "
                   "for confirmation and proper treatment.")
        elif confidence >= 60:
            return ("This is a preliminary assessment with moderate confidence. "
                   "Strongly recommended to consult a healthcare professional "
                   "for accurate diagnosis and treatment.")
        else:
            return ("This assessment has low confidence. "
                   "It is ESSENTIAL to consult a qualified healthcare provider "
                   "for proper diagnosis and treatment. Do not rely solely on this assessment.")
