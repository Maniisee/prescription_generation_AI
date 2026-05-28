#!/usr/bin/env python3
"""
Test script for AI Prescription Generator
Shows comparison between rule-based and AI-generated prescriptions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.prescription_generator import PrescriptionGenerator
from models.ai_prescription_generator import (
    AIPrescriptionGenerator,
    LocalLLMPrescriptionGenerator,
    HybridPrescriptionGenerator
)

# Test data
test_diagnosis = {
    'disease': 'Flu',
    'confidence': 85.5,
    'severity': 'medium',
    'matched_symptoms': ['fever', 'cough', 'body aches', 'fatigue'],
    'vitals': {
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80,
        'temperature': 101.5,
        'pulse': 95
    }
}

test_patient = {
    'name': 'John Doe',
    'age': 35,
    'gender': 'male',
    'medical_history': 'No known allergies. Previous history of asthma.'
}

def print_prescription(title, prescription):
    """Pretty print prescription"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")
    
    print("\n💊 MEDICATIONS:")
    for med in prescription.get('medications', []):
        print(f"  • {med.get('name', 'N/A')}")
        print(f"    Dosage: {med.get('dosage', 'N/A')}")
        print(f"    Frequency: {med.get('frequency', 'N/A')}")
        print(f"    Duration: {med.get('duration', 'N/A')}")
        print()
    
    print("\n📋 INSTRUCTIONS:")
    for instruction in prescription.get('instructions', []):
        print(f"  • {instruction}")
    
    print("\n⚠️  PRECAUTIONS:")
    for precaution in prescription.get('precautions', []):
        print(f"  • {precaution}")
    
    if 'ai_recommendations' in prescription:
        print("\n🤖 AI PERSONALIZED ADVICE:")
        for advice in prescription.get('ai_recommendations', {}).get('advice', []):
            print(f"  • {advice}")
    
    if 'lifestyle_recommendations' in prescription:
        print("\n🏃 LIFESTYLE RECOMMENDATIONS:")
        for rec in prescription.get('lifestyle_recommendations', []):
            print(f"  • {rec}")
    
    print(f"\n⚕️  DISCLAIMER:")
    print(f"  {prescription.get('disclaimer', 'Consult a healthcare professional.')}")
    print()


def test_rule_based():
    """Test original rule-based generator"""
    print("\n🔧 Testing RULE-BASED Generator...")
    generator = PrescriptionGenerator()
    prescription = generator.generate(test_diagnosis, test_patient)
    print_prescription("RULE-BASED PRESCRIPTION", prescription)
    return prescription


def test_ai_openai():
    """Test OpenAI-powered generator"""
    print("\n🤖 Testing OPENAI Generator...")
    generator = AIPrescriptionGenerator()
    
    if not generator.use_ai:
        print("❌ OpenAI not configured. Set OPENAI_API_KEY environment variable.")
        print("   Get key from: https://platform.openai.com/api-keys")
        return None
    
    try:
        prescription = generator.generate(test_diagnosis, test_patient)
        print_prescription("AI-GENERATED PRESCRIPTION (OpenAI GPT)", prescription)
        return prescription
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_local_llm():
    """Test local LLM generator (Ollama)"""
    print("\n💻 Testing LOCAL LLM Generator (Ollama)...")
    generator = LocalLLMPrescriptionGenerator()
    
    if not generator.use_local:
        print("❌ Ollama not running. Install from: https://ollama.ai")
        print("   Then run: ollama pull llama3")
        return None
    
    try:
        prescription = generator.generate(test_diagnosis, test_patient)
        print_prescription("LOCAL LLM PRESCRIPTION (Ollama)", prescription)
        return prescription
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_hybrid():
    """Test hybrid generator"""
    print("\n🔀 Testing HYBRID Generator (Rule-based + AI Enhancement)...")
    generator = HybridPrescriptionGenerator()
    
    try:
        prescription = generator.generate(test_diagnosis, test_patient)
        print_prescription("HYBRID PRESCRIPTION", prescription)
        return prescription
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("  AI PRESCRIPTION GENERATOR TEST SUITE")
    print("="*80)
    print(f"\n📊 Test Case:")
    print(f"  Disease: {test_diagnosis['disease']}")
    print(f"  Confidence: {test_diagnosis['confidence']}%")
    print(f"  Patient: {test_patient['name']}, {test_patient['age']}y/o {test_patient['gender']}")
    print(f"  Symptoms: {', '.join(test_diagnosis['matched_symptoms'])}")
    
    results = {}
    
    # Test 1: Rule-based (always works)
    results['rule_based'] = test_rule_based()
    
    # Test 2: OpenAI (if configured)
    results['openai'] = test_ai_openai()
    
    # Test 3: Local LLM (if Ollama running)
    results['local_llm'] = test_local_llm()
    
    # Test 4: Hybrid (if AI available)
    results['hybrid'] = test_hybrid()
    
    # Summary
    print("\n" + "="*80)
    print("  TEST SUMMARY")
    print("="*80)
    print(f"\n✅ Rule-based: Working")
    print(f"{'✅' if results['openai'] else '❌'} OpenAI GPT: {'Working' if results['openai'] else 'Not configured'}")
    print(f"{'✅' if results['local_llm'] else '❌'} Local LLM: {'Working' if results['local_llm'] else 'Not available'}")
    print(f"{'✅' if results['hybrid'] else '❌'} Hybrid: {'Working' if results['hybrid'] else 'Not available'}")
    
    print("\n💡 Next Steps:")
    if not results['openai']:
        print("  1. Get OpenAI API key: https://platform.openai.com/api-keys")
        print("  2. Set environment variable: export OPENAI_API_KEY='sk-your-key'")
        print("  3. Run: pip install openai")
    if not results['local_llm']:
        print("  1. Install Ollama: https://ollama.ai")
        print("  2. Run: ollama pull llama3")
        print("  3. Start: ollama serve")
    
    print("\n📖 For more details, see: AI_INTEGRATION_GUIDE.md")
    print()


if __name__ == "__main__":
    main()
