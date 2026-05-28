"""
Prescription Generator
Generates treatment recommendations based on diagnosis
"""

class PrescriptionGenerator:
    def __init__(self):
        self.treatment_database = self.load_treatment_database()
    
    def load_treatment_database(self):
        """Load disease treatment protocols"""
        return {
            'Common Cold': {
                'medications': [
                    {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'Every 6 hours'},
                    {'name': 'Cetirizine', 'dosage': '10mg', 'frequency': 'Once daily'},
                    {'name': 'Vitamin C', 'dosage': '500mg', 'frequency': 'Twice daily'}
                ],
                'instructions': 'Rest adequately, stay hydrated, avoid cold exposure',
                'precautions': 'Avoid self-medication beyond 3 days. Consult doctor if symptoms worsen.',
                'duration': '5-7 days'
            },
            'Flu': {
                'medications': [
                    {'name': 'Paracetamol', 'dosage': '650mg', 'frequency': 'Every 6 hours'},
                    {'name': 'Oseltamivir', 'dosage': '75mg', 'frequency': 'Twice daily'},
                    {'name': 'Multivitamin', 'dosage': '1 tablet', 'frequency': 'Once daily'}
                ],
                'instructions': 'Complete bed rest, increase fluid intake, maintain good hygiene',
                'precautions': 'Monitor temperature. Seek immediate care if breathing difficulty occurs.',
                'duration': '7-10 days'
            },
            'Diabetes': {
                'medications': [
                    {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily after meals'},
                    {'name': 'Glimepiride', 'dosage': '1mg', 'frequency': 'Once before breakfast'}
                ],
                'instructions': 'Follow diabetic diet, regular exercise, monitor blood sugar levels',
                'precautions': 'Regular HbA1c testing required. Avoid skipping meals. Carry glucose candies.',
                'duration': 'Long-term management'
            },
            'Hypertension': {
                'medications': [
                    {'name': 'Amlodipine', 'dosage': '5mg', 'frequency': 'Once daily'},
                    {'name': 'Atenolol', 'dosage': '50mg', 'frequency': 'Once daily'}
                ],
                'instructions': 'Low salt diet, regular exercise, stress management, regular BP monitoring',
                'precautions': 'Do not stop medication suddenly. Regular health checkups required.',
                'duration': 'Long-term management'
            },
            'Asthma': {
                'medications': [
                    {'name': 'Salbutamol Inhaler', 'dosage': '2 puffs', 'frequency': 'As needed'},
                    {'name': 'Montelukast', 'dosage': '10mg', 'frequency': 'Once daily at bedtime'},
                    {'name': 'Budesonide Inhaler', 'dosage': '200mcg', 'frequency': 'Twice daily'}
                ],
                'instructions': 'Avoid triggers, use inhaler correctly, maintain peak flow diary',
                'precautions': 'Carry rescue inhaler always. Seek emergency care if severe attack.',
                'duration': 'Long-term management'
            },
            'Migraine': {
                'medications': [
                    {'name': 'Sumatriptan', 'dosage': '50mg', 'frequency': 'At onset of attack'},
                    {'name': 'Naproxen', 'dosage': '500mg', 'frequency': 'Twice daily with food'},
                    {'name': 'Propranolol', 'dosage': '40mg', 'frequency': 'Twice daily (preventive)'}
                ],
                'instructions': 'Rest in dark quiet room, avoid triggers, maintain sleep schedule',
                'precautions': 'Track migraine triggers. Limit pain medication to prevent rebound headaches.',
                'duration': 'As needed / Preventive ongoing'
            },
            'Gastritis': {
                'medications': [
                    {'name': 'Pantoprazole', 'dosage': '40mg', 'frequency': 'Once before breakfast'},
                    {'name': 'Sucralfate', 'dosage': '1g', 'frequency': 'Before meals'},
                    {'name': 'Domperidone', 'dosage': '10mg', 'frequency': 'Before meals'}
                ],
                'instructions': 'Avoid spicy foods, eat small frequent meals, reduce stress',
                'precautions': 'Avoid alcohol and NSAIDs. If symptoms persist beyond 2 weeks, get endoscopy.',
                'duration': '4-6 weeks'
            },
            'Pneumonia': {
                'medications': [
                    {'name': 'Azithromycin', 'dosage': '500mg', 'frequency': 'Once daily'},
                    {'name': 'Amoxicillin-Clavulanate', 'dosage': '625mg', 'frequency': 'Thrice daily'},
                    {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'Every 6 hours'}
                ],
                'instructions': 'Complete antibiotic course, rest, increase fluid intake, breathing exercises',
                'precautions': 'Hospital admission may be needed for severe cases. Monitor oxygen levels.',
                'duration': '7-14 days'
            },
            'Allergic Rhinitis': {
                'medications': [
                    {'name': 'Cetirizine', 'dosage': '10mg', 'frequency': 'Once daily at night'},
                    {'name': 'Fluticasone nasal spray', 'dosage': '2 sprays/nostril', 'frequency': 'Once daily'},
                    {'name': 'Montelukast', 'dosage': '10mg', 'frequency': 'Once daily'}
                ],
                'instructions': 'Avoid allergens, keep environment clean, use air purifiers',
                'precautions': 'Identify and avoid specific triggers. Consider allergy testing.',
                'duration': 'As needed / Seasonal'
            },
            'Bronchitis': {
                'medications': [
                    {'name': 'Amoxicillin', 'dosage': '500mg', 'frequency': 'Thrice daily'},
                    {'name': 'Bromhexine', 'dosage': '8mg', 'frequency': 'Thrice daily'},
                    {'name': 'Salbutamol syrup', 'dosage': '5ml', 'frequency': 'Thrice daily'}
                ],
                'instructions': 'Rest, increase fluids, avoid smoke/pollution, steam inhalation',
                'precautions': 'Complete antibiotic course. Seek care if breathing worsens.',
                'duration': '7-10 days'
            }
        }
    
    def generate(self, diagnosis, patient):
        """
        Generate prescription based on diagnosis
        Returns: {medications, dosage, instructions, precautions, duration}
        """
        disease = diagnosis.get('disease')
        
        if disease not in self.treatment_database:
            return self.generate_generic_prescription(diagnosis)
        
        treatment = self.treatment_database[disease]
        
        # Customize based on patient factors
        customized = self.customize_prescription(treatment, patient, diagnosis)
        
        return customized
    
    def customize_prescription(self, treatment, patient, diagnosis):
        """Customize prescription based on patient factors"""
        # Base prescription
        prescription = {
            'medications': treatment['medications'],
            'general_dosage': f"Duration: {treatment['duration']}",
            'instructions': treatment['instructions'],
            'precautions': treatment['precautions']
        }
        
        # Add age-specific modifications
        age = patient.get('age', 0)
        if age < 18:
            prescription['precautions'] += ' Pediatric dosing - consult pediatrician.'
        elif age > 65:
            prescription['precautions'] += ' Elderly patient - monitor for drug interactions.'
        
        # Add confidence-based disclaimer
        confidence = diagnosis.get('confidence', 0)
        if confidence < 70:
            prescription['precautions'] = f"LOW CONFIDENCE PREDICTION ({confidence}%). " + prescription['precautions']
            prescription['instructions'] = "IMMEDIATE MEDICAL CONSULTATION STRONGLY RECOMMENDED. " + prescription['instructions']
        
        # Add vital signs alerts
        if 'vitals' in diagnosis:
            vitals = diagnosis['vitals']
            
            bp_sys = vitals.get('blood_pressure_systolic', 0)
            if bp_sys > 140:
                prescription['precautions'] += ' HIGH BLOOD PRESSURE DETECTED - Urgent medical evaluation needed.'
            
            temp = vitals.get('temperature', 0)
            if temp > 102:
                prescription['precautions'] += ' HIGH FEVER - Monitor closely, seek care if persists.'
        
        # Add general disclaimer
        prescription['disclaimer'] = """
        ⚠️ IMPORTANT DISCLAIMER:
        This is an AI-generated preliminary prescription for informational purposes only.
        It is NOT a substitute for professional medical advice.
        ALWAYS consult a licensed healthcare provider before starting any medication.
        In case of emergency, call emergency services immediately.
        """
        
        return prescription
    
    def generate_generic_prescription(self, diagnosis):
        """Generate generic prescription for unknown diseases"""
        return {
            'medications': [
                {'name': 'Symptomatic treatment', 'dosage': 'As directed', 'frequency': 'As prescribed'}
            ],
            'general_dosage': 'Consult healthcare provider',
            'instructions': 'Seek immediate medical consultation for proper diagnosis and treatment',
            'precautions': 'Do not self-medicate. Professional medical evaluation required.',
            'disclaimer': """
            ⚠️ MEDICAL CONSULTATION REQUIRED:
            The symptoms provided do not match known disease patterns with sufficient confidence.
            Please visit a healthcare professional for proper diagnosis and treatment.
            """
        }
    
    def format_prescription_text(self, prescription):
        """Format prescription as readable text"""
        text = "PRESCRIPTION\n"
        text += "=" * 60 + "\n\n"
        
        text += "MEDICATIONS:\n"
        for i, med in enumerate(prescription['medications'], 1):
            text += f"{i}. {med['name']}\n"
            text += f"   Dosage: {med['dosage']}\n"
            text += f"   Frequency: {med['frequency']}\n\n"
        
        text += f"DURATION: {prescription['general_dosage']}\n\n"
        text += f"INSTRUCTIONS:\n{prescription['instructions']}\n\n"
        text += f"PRECAUTIONS:\n{prescription['precautions']}\n\n"
        text += prescription.get('disclaimer', '')
        
        return text
