#!/usr/bin/env python3
"""
Demonstration: How Ollama Generates Prescriptions
Shows the exact prompt and data flow
"""

def show_prompt_generation():
    """Demonstrates how data becomes a prompt for Ollama"""
    
    print("\n" + "="*80)
    print("  HOW OLLAMA GENERATES PRESCRIPTIONS - DETAILED FLOW")
    print("="*80)
    
    # Step 1: Show input data
    print("\n" + "─"*80)
    print("STEP 1: INPUT DATA (From Patient Form)")
    print("─"*80)
    
    diagnosis = {
        'disease': 'Flu',
        'confidence': 85.5,
        'severity': 'medium',
        'matched_symptoms': ['fever', 'cough', 'body aches', 'headache', 'fatigue'],
        'vitals': {
            'blood_pressure_systolic': 120,
            'blood_pressure_diastolic': 80,
            'temperature': 101.5,
            'pulse': 95
        }
    }
    
    patient = {
        'name': 'John Doe',
        'age': 35,
        'gender': 'male',
        'medical_history': 'History of asthma. No known drug allergies.'
    }
    
    print("\n📊 Diagnosis Data:")
    for key, value in diagnosis.items():
        print(f"  • {key}: {value}")
    
    print("\n👤 Patient Data:")
    for key, value in patient.items():
        print(f"  • {key}: {value}")
    
    # Step 2: Build the prompt
    print("\n" + "─"*80)
    print("STEP 2: BUILDING THE PROMPT (Instructions to AI)")
    print("─"*80)
    
    prompt = f"""Generate a treatment prescription for the following case:

**Diagnosis:**
- Disease: {diagnosis.get('disease')}
- Confidence: {diagnosis.get('confidence')}%
- Severity: {diagnosis.get('severity')}
- Symptoms: {', '.join(diagnosis.get('matched_symptoms', []))}

**Patient Information:**
- Age: {patient.get('age')} years
- Gender: {patient.get('gender')}
- Medical History: {patient.get('medical_history')}

**Vitals:**
- Blood Pressure: {diagnosis.get('vitals', {}).get('blood_pressure_systolic')}/{diagnosis.get('vitals', {}).get('blood_pressure_diastolic')} mmHg
- Temperature: {diagnosis.get('vitals', {}).get('temperature')}°F
- Pulse: {diagnosis.get('vitals', {}).get('pulse')} bpm

Please provide treatment recommendations in this JSON format:
{{
    "medications": [
        {{"name": "Medicine Name", "dosage": "Amount", "frequency": "How often", "duration": "How long"}}
    ],
    "instructions": ["Instruction 1", "Instruction 2", ...],
    "precautions": ["Precaution 1", "Precaution 2", ...],
    "lifestyle_recommendations": ["Recommendation 1", "Recommendation 2", ...],
    "follow_up": "When to follow up with doctor",
    "disclaimer": "Medical disclaimer"
}}

Focus on evidence-based treatments. Consider patient age and medical history."""
    
    print("\n📝 Full Prompt Sent to Ollama:")
    print("┌" + "─"*78 + "┐")
    for line in prompt.split('\n'):
        print(f"│ {line:<76} │")
    print("└" + "─"*78 + "┘")
    
    # Step 3: Show what Ollama does
    print("\n" + "─"*80)
    print("STEP 3: OLLAMA PROCESSING")
    print("─"*80)
    
    print("\n🤖 What Ollama Does:")
    print("  1. Receives the prompt (text above)")
    print("  2. Loads LLaMA 3 neural network model into memory")
    print("  3. Tokenizes the prompt (converts text to numbers)")
    print("  4. Runs through ~8 billion parameters of the model")
    print("  5. Generates response token by token")
    print("  6. Formats response as JSON")
    print("  7. Returns the prescription")
    
    print("\n📊 Data Used by Ollama:")
    print("  ✓ Disease name → Identifies treatment protocols")
    print("  ✓ Symptoms → Validates treatment relevance")
    print("  ✓ Patient age → Adjusts dosages (pediatric/elderly)")
    print("  ✓ Gender → Considers gender-specific factors")
    print("  ✓ Medical history → Avoids contraindications")
    print("  ✓ Vitals → Assesses severity, adjusts treatment")
    print("  ✓ Confidence level → Affects recommendation strength")
    
    print("\n🧠 How AI 'Knows' About Medicine:")
    print("  • LLaMA 3 was trained on billions of text documents")
    print("  • Training included medical literature, textbooks, journals")
    print("  • Model learned patterns: 'flu' → 'oseltamivir, rest, fluids'")
    print("  • It 'memorized' treatment protocols during training")
    print("  • NOT searching internet - using trained knowledge")
    
    # Step 4: Show example response
    print("\n" + "─"*80)
    print("STEP 4: OLLAMA'S RESPONSE")
    print("─"*80)
    
    example_response = {
        "medications": [
            {
                "name": "Oseltamivir (Tamiflu)",
                "dosage": "75mg",
                "frequency": "Twice daily (morning and evening)",
                "duration": "5 days"
            },
            {
                "name": "Paracetamol (Tylenol)",
                "dosage": "650mg",
                "frequency": "Every 6 hours as needed",
                "duration": "Until fever subsides"
            },
            {
                "name": "Guaifenesin (Mucinex)",
                "dosage": "400mg",
                "frequency": "Every 4 hours",
                "duration": "7 days"
            }
        ],
        "instructions": [
            "Complete bed rest for at least 3-4 days",
            "Drink plenty of fluids (8-10 glasses of water daily)",
            "Use a humidifier in your room to ease breathing",
            "Take medications with food to prevent stomach upset",
            "Monitor temperature every 6 hours",
            "Isolate yourself from others to prevent spread"
        ],
        "precautions": [
            "Keep your asthma inhaler readily available",
            "Watch for worsening breathing difficulty - seek immediate care if severe",
            "Avoid cold air exposure which may trigger asthma symptoms",
            "Do not stop medications without completing the full course",
            "Seek emergency care if fever exceeds 103°F or breathing becomes labored"
        ],
        "lifestyle_recommendations": [
            "Maintain room temperature between 68-72°F",
            "Eat light, easily digestible foods (soups, broths)",
            "Avoid dairy products if they increase mucus production",
            "Get plenty of sleep - aim for 8-10 hours per night",
            "Consider vitamin C supplements (1000mg daily) to support recovery"
        ],
        "follow_up": "Schedule a follow-up with your doctor if symptoms persist beyond 7 days or worsen after initial improvement",
        "disclaimer": "This is an AI-generated recommendation based on your symptoms and medical history. It does not replace professional medical advice. Always consult with a licensed healthcare provider before starting any treatment."
    }
    
    print("\n📋 Generated Prescription (JSON):")
    import json
    print(json.dumps(example_response, indent=2))
    
    # Step 5: Key Insights
    print("\n" + "─"*80)
    print("STEP 5: KEY INSIGHTS")
    print("─"*80)
    
    print("\n🎯 How AI Personalizes the Prescription:")
    print("\n  CONSIDERS:")
    print("  ✓ Age (35) → Adult dosage, no pediatric adjustments")
    print("  ✓ Gender (male) → Standard treatment (no pregnancy concerns)")
    print("  ✓ Asthma history → Added inhaler reminder & breathing precautions")
    print("  ✓ High fever (101.5°F) → Included antipyretics, monitoring")
    print("  ✓ Multiple symptoms → Multi-drug approach (antiviral + symptomatic)")
    print("  ✓ Flu diagnosis → Evidence-based: Tamiflu within 48 hours")
    
    print("\n  AVOIDS:")
    print("  ✗ Aspirin (age >35, no pediatric risk but unnecessary)")
    print("  ✗ NSAIDs without food instruction (GI protection)")
    print("  ✗ Aggressive steroids (asthma stable, not needed for flu)")
    print("  ✗ Antibiotics (viral infection, not bacterial)")
    
    print("\n💡 Comparison: Rule-Based vs AI:")
    print("\n  RULE-BASED (Current):")
    print("  • Uses predefined database: IF disease='Flu' THEN medications=[...]")
    print("  • Same prescription for everyone with flu")
    print("  • Fast, reliable, validated by doctors")
    print("  • Cannot adapt to unique patient factors")
    
    print("\n  AI-BASED (Ollama):")
    print("  • Analyzes ALL input data together")
    print("  • Considers interactions: age + history + vitals + symptoms")
    print("  • Different prescription for 35yo with asthma vs 65yo with diabetes")
    print("  • More personalized, but requires validation")
    
    print("\n🔒 Safety Considerations:")
    print("  • AI suggestions should be reviewed by doctors")
    print("  • Hybrid approach recommended: Rule-based + AI enhancement")
    print("  • Always include medical disclaimer")
    print("  • Log all AI-generated prescriptions for audit")
    
    # Step 6: Technical Details
    print("\n" + "─"*80)
    print("STEP 6: TECHNICAL DETAILS")
    print("─"*80)
    
    print("\n🔧 HTTP Request to Ollama:")
    print("""
    POST http://localhost:11434/api/generate
    Content-Type: application/json
    
    {
        "model": "llama3",
        "prompt": "<full prompt from Step 2>",
        "stream": false,
        "format": "json",
        "temperature": 0.3
    }
    """)
    
    print("\n⚙️  Parameters Explained:")
    print("  • model: 'llama3' → Which AI model to use")
    print("  • prompt: The full text instructions")
    print("  • stream: false → Get complete response at once")
    print("  • format: 'json' → Return structured data, not plain text")
    print("  • temperature: 0.3 → Low = more consistent (0-1 scale)")
    print("       ↳ 0.0 = Always same answer (deterministic)")
    print("       ↳ 0.3 = Slight variation (recommended for medical)")
    print("       ↳ 1.0 = Creative/random (bad for prescriptions)")
    
    print("\n⏱️  Performance:")
    print("  • First request: ~15 seconds (loading model)")
    print("  • Subsequent: ~5-10 seconds")
    print("  • Model stays in RAM after first use")
    print("  • Uses ~6GB RAM while running")
    
    print("\n💾 Where Ollama Stores Data:")
    print("  • Models: ~/.ollama/models/")
    print("  • Logs: ~/.ollama/logs/")
    print("  • No patient data is stored by Ollama")
    print("  • All processing is real-time, no history kept")
    
    print("\n" + "="*80)
    print("  Summary")
    print("="*80)
    print("""
The prescription generation flow:

Patient Form → Flask Backend → AI Generator
    ↓
Build Prompt (combine all patient data)
    ↓
Send to Ollama (http://localhost:11434)
    ↓
LLaMA 3 Model processes prompt
    ↓
Generate personalized prescription
    ↓
Return JSON response
    ↓
Save to Database → Display to User

Key Insight: The AI doesn't "learn" from your patients. It uses knowledge
from its training (medical literature) to generate recommendations based
on the specific patient data you provide in the prompt.
""")


if __name__ == "__main__":
    show_prompt_generation()
    
    print("\n🚀 Want to see this in action?")
    print("   1. Install Ollama: https://ollama.ai")
    print("   2. Run: ollama pull llama3")
    print("   3. Run: python test_ai_generator.py")
    print()
