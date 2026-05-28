#!/usr/bin/env python3
"""
Direct test of AI Disease Classifier without database
"""

import sys
sys.path.insert(0, '/Users/manikandank/Downloads/disease_detection_ai')

from models.disease_classifier import DiseaseClassifier
from models.prescription_generator import PrescriptionGenerator

# Initialize models
classifier = DiseaseClassifier()
prescription_gen = PrescriptionGenerator()

print("=" * 60)
print("🏥 AI DISEASE DETECTION SYSTEM - DIRECT TEST")
print("=" * 60)

# Test case 1: Flu symptoms
print("\n📋 TEST CASE 1: Flu Symptoms")
print("-" * 60)
symptoms = ['fever', 'cough', 'body aches', 'headache', 'fatigue']
vitals = {
    'blood_pressure_systolic': 130,
    'blood_pressure_diastolic': 85,
    'temperature': 102,
    'pulse': 85
}
patient = {
    'age': 30,
    'gender': 'male'
}

print(f"Symptoms: {', '.join(symptoms)}")
print(f"Temperature: {vitals['temperature']}°F")
print(f"BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']}")
print(f"Pulse: {vitals['pulse']} bpm")

# Get diagnosis
diagnosis = classifier.predict(symptoms, vitals, patient)

print(f"\n✅ DIAGNOSIS:")
print(f"   Disease: {diagnosis['disease']}")
print(f"   Confidence: {diagnosis['confidence']:.1f}%")
print(f"   Severity: {diagnosis['severity']}")
print(f"   Matched Symptoms: {', '.join(diagnosis['matched_symptoms'])}")

if diagnosis['alternatives']:
    print(f"\n🔍 ALTERNATIVE POSSIBILITIES:")
    for alt in diagnosis['alternatives']:
        print(f"   - {alt['disease']}: {alt['confidence']:.1f}%")

# Generate prescription
prescription = prescription_gen.generate(diagnosis, patient)

print(f"\n💊 PRESCRIPTION:")
print(f"   Medications:")
for med in prescription['medications']:
    print(f"   - {med['name']}: {med['dosage']} - {med['frequency']}")

print(f"\n📋 INSTRUCTIONS:")
for instruction in prescription['instructions'][:3]:
    print(f"   • {instruction}")

print(f"\n⚠️  PRECAUTIONS:")
for precaution in prescription['precautions'][:3]:
    print(f"   • {precaution}")

# Test case 2: Diabetes symptoms
print("\n" + "=" * 60)
print("📋 TEST CASE 2: Diabetes Symptoms")
print("-" * 60)
symptoms2 = ['increased thirst', 'frequent urination', 'fatigue', 'blurred vision']
vitals2 = {
    'blood_pressure_systolic': 145,
    'blood_pressure_diastolic': 92,
    'temperature': 98.6,
    'pulse': 78
}
patient2 = {
    'age': 55,
    'gender': 'male'
}

print(f"Symptoms: {', '.join(symptoms2)}")
print(f"Age: {patient2['age']}")

diagnosis2 = classifier.predict(symptoms2, vitals2, patient2)
print(f"\n✅ DIAGNOSIS:")
print(f"   Disease: {diagnosis2['disease']}")
print(f"   Confidence: {diagnosis2['confidence']:.1f}%")
print(f"   Severity: {diagnosis2['severity']}")

prescription2 = prescription_gen.generate(diagnosis2, patient2)
print(f"\n💊 PRESCRIPTION:")
for med in prescription2['medications'][:2]:
    print(f"   - {med['name']}: {med['dosage']} - {med['frequency']}")

print("\n" + "=" * 60)
print("✅ AI MODEL TEST COMPLETED SUCCESSFULLY!")
print("=" * 60)
