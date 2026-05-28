"""
AI-Powered Prescription Generator using OpenAI GPT
Generates personalized treatment recommendations using LLM
"""

import os
from typing import Dict, List
import json

class AIPrescriptionGenerator:
    """
    Generates prescriptions using OpenAI GPT API
    Falls back to rule-based if API unavailable
    """
    
    def __init__(self):
        """Initialize with OpenAI API key"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.use_ai = bool(self.api_key)
        
        if self.use_ai:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                print("OpenAI package not installed. Run: pip install openai")
                self.use_ai = False
        
        # Fallback to rule-based generator
        if not self.use_ai:
            from models.prescription_generator import PrescriptionGenerator
            self.fallback_generator = PrescriptionGenerator()
    
    def generate(self, diagnosis: Dict, patient: Dict = None) -> Dict:
        """
        Generate prescription using AI or fallback to rules
        
        Args:
            diagnosis: {disease, confidence, severity, symptoms, vitals}
            patient: {name, age, gender, medical_history}
        
        Returns:
            {medications, instructions, precautions, disclaimer}
        """
        if self.use_ai:
            try:
                return self._generate_with_ai(diagnosis, patient)
            except Exception as e:
                print(f"AI generation failed: {e}, using fallback")
                return self.fallback_generator.generate(diagnosis, patient)
        else:
            return self.fallback_generator.generate(diagnosis, patient)
    
    def _generate_with_ai(self, diagnosis: Dict, patient: Dict) -> Dict:
        """Generate prescription using OpenAI GPT"""
        
        # Build prompt
        prompt = self._build_prompt(diagnosis, patient)
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for lower cost
            messages=[
                {
                    "role": "system",
                    "content": """You are an experienced medical AI assistant. 
                    Generate treatment recommendations in JSON format.
                    Include medications with dosage, frequency, and duration.
                    Provide clear instructions and precautions.
                    Always add disclaimer to consult a real doctor."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for consistent medical advice
            response_format={"type": "json_object"}
        )
        
        # Parse response
        result = json.loads(response.choices[0].message.content)
        
        # Ensure proper format
        return self._format_response(result)
    
    def _build_prompt(self, diagnosis: Dict, patient: Dict) -> str:
        """Build prompt for LLM"""
        
        # Extract symptoms (could be list or JSON string from database)
        symptoms = diagnosis.get('symptoms', [])
        if isinstance(symptoms, str):
            import json
            try:
                symptoms = json.loads(symptoms)
            except:
                symptoms = []
        
        # Extract vitals (could be dict or JSON string from database)
        vitals = diagnosis.get('vitals', {})
        if isinstance(vitals, str):
            import json
            try:
                vitals = json.loads(vitals)
            except:
                vitals = {}
        
        # Handle matched_symptoms from prediction or symptoms from database
        symptom_list = diagnosis.get('matched_symptoms', symptoms)
        if isinstance(symptom_list, list):
            symptoms_text = ', '.join(symptom_list) if symptom_list else 'None reported'
        else:
            symptoms_text = str(symptom_list)
        
        prompt = f"""Generate a treatment prescription for the following case:

**Diagnosis:**
- Disease: {diagnosis.get('disease', 'Unknown')}
- Confidence: {diagnosis.get('confidence', 0)}%
- Severity: {diagnosis.get('severity', 'medium')}
- Symptoms: {symptoms_text}

**Patient Information:**
- Age: {patient.get('age', 'Unknown')} years
- Gender: {patient.get('gender', 'Unknown')}
- Medical History: {patient.get('medical_history', 'None reported')}

**Vitals:**
- Blood Pressure: {vitals.get('blood_pressure_systolic', 'N/A')}/{vitals.get('blood_pressure_diastolic', 'N/A')} mmHg
- Temperature: {vitals.get('temperature', 'N/A')}°F
- Pulse: {vitals.get('pulse', 'N/A')} bpm

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
        
        return prompt
    
    def _format_response(self, result: Dict) -> Dict:
        """Ensure response has required format"""
        return {
            'medications': result.get('medications', []),
            'instructions': result.get('instructions', []),
            'precautions': result.get('precautions', []),
            'lifestyle_recommendations': result.get('lifestyle_recommendations', []),
            'follow_up': result.get('follow_up', 'Consult doctor within 1 week'),
            'disclaimer': result.get('disclaimer', 
                'This is an AI-generated recommendation. Always consult a licensed healthcare professional.')
        }


class LocalLLMPrescriptionGenerator:
    """
    Generate prescriptions using local LLM (Ollama, LLaMA, etc.)
    No API key needed, runs on your computer
    """
    
    def __init__(self, model_name: str = "llama3"):
        """
        Initialize with local model - OLLAMA ONLY, NO FALLBACK
        Requires Ollama running: https://ollama.ai
        """
        self.model_name = model_name
        # Check if Ollama is available
        if not self._check_ollama():
            raise RuntimeError(
                "❌ Ollama is not running! Start it with: ollama serve\n"
                "LLaMA 3 is required for prescription generation. No fallback available."
            )
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running and has llama3 model"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                # Check if llama3 model exists
                has_llama3 = any("llama3" in m.get("name", "") for m in models)
                if has_llama3:
                    return True
                else:
                    raise RuntimeError("LLaMA 3 model not found. Run: ollama pull llama3")
            return False
        except Exception as e:
            raise RuntimeError(f"Cannot connect to Ollama: {e}")
    
    def generate(self, diagnosis: Dict, patient: Dict = None) -> Dict:
        """Generate prescription using LLaMA 3 ONLY - no fallback"""
        import sys
        
        sys.stderr.write("\n" + "="*60 + "\n")
        sys.stderr.write("🤖 USING LLaMA 3 FOR PRESCRIPTION GENERATION\n")
        sys.stderr.write("="*60 + "\n")
        sys.stderr.flush()
        
        try:
            result = self._generate_with_ollama(diagnosis, patient)
            sys.stderr.write("\n✅ LLaMA 3 successfully generated prescription\n\n")
            sys.stderr.flush()
            return result
        except Exception as e:
            sys.stderr.write(f"\n❌ LLaMA 3 FAILED: {e}\n\n")
            sys.stderr.flush()
            raise RuntimeError(f"LLaMA 3 prescription generation failed: {e}. No fallback available.")
    def _generate_with_ollama(self, diagnosis: Dict, patient: Dict) -> Dict:
        """Call local Ollama API - ULTRA FAST version"""
        import requests
        import re
        import sys
        
        disease = diagnosis.get('disease', 'Unknown')
        age = patient.get('age', 30) if patient else 30
        
        # Simple structured prompt that LLaMA 3 can follow
        prompt = f"""You are a medical assistant. For {disease} in a {age} year old, provide:

MEDICATION: [name] | [dosage] | [frequency] | [duration]
INSTRUCTION: [brief instruction]
PRECAUTION: [brief precaution]

Be concise. Use this exact format."""
        
        # Call Ollama WITHOUT strict JSON format (much faster)
        sys.stderr.write(f"   → Asking LLaMA 3 about {disease}...\n")
        sys.stderr.flush()
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower for more consistent output
                    "num_predict": 400   # Shorter for speed
                }
            },
            timeout=30
        )
        
        result = response.json()
        text = result['response']
        
        sys.stderr.write(f"   → LLaMA 3 responded ({len(text)} chars)\n")
        sys.stderr.write(f"   → FULL Raw response:\n{text}\n")
        sys.stderr.write(f"   → END OF RAW RESPONSE\n")
        sys.stderr.flush()
        
        # NEW METHOD: Parse structured text format with flexible matching
        if 'MEDICATION' in text.upper() or 'INSTRUCTION' in text.upper():
            sys.stderr.write(f"   → Parsing structured text format\n")
            sys.stderr.flush()
            
            medications = []
            instructions = []
            precautions = []
            
            lines = text.split('\n')
            current_section = None
            
            for line in lines:
                line_stripped = line.strip()
                line_upper = line_stripped.upper()
                
                # Check for INSTRUCTION: or PRECAUTION: with content on same line
                if 'INSTRUCTION:' in line_upper:
                    # Extract everything after "INSTRUCTION:"
                    idx = line_upper.index('INSTRUCTION:')
                    content = line_stripped[idx + 12:].strip()
                    if content:
                        instructions.append(content)
                    continue
                
                if 'PRECAUTION:' in line_upper:
                    # Extract everything after "PRECAUTION:"
                    idx = line_upper.index('PRECAUTION:')
                    content = line_stripped[idx + 11:].strip()
                    if content:
                        precautions.append(content)
                    continue
                
                # Detect section headers (with or without markdown)
                if '**MEDICATION' in line_upper or (current_section != 'medication' and 'MEDICATION:' in line_upper):
                    current_section = 'medication'
                    continue
                
                # Parse medication content
                if line_stripped and '|' in line_stripped:
                    # Handle bullet points: "* Medication | dosage | frequency | duration"
                    med_line = line_stripped
                    if med_line.startswith('*') or med_line.startswith('-'):
                        med_line = med_line[1:].strip()
                    
                    # Split by pipe delimiter
                    parts = med_line.split('|')
                    if len(parts) >= 4:
                        medications.append({
                            'name': parts[0].strip(),
                            'dosage': parts[1].strip(),
                            'frequency': parts[2].strip(),
                            'duration': parts[3].strip()
                        })
                
                # Legacy: check if we're still in a section context
                elif current_section == 'instruction' and line_stripped:
                    if line_stripped.startswith('*') or line_stripped.startswith('-'):
                        line_stripped = line_stripped[1:].strip()
                    if line_stripped and not line_stripped.startswith('**'):
                        instructions.append(line_stripped)
                
                elif current_section == 'precaution' and line_stripped:
                    if line_stripped.startswith('*') or line_stripped.startswith('-'):
                        line_stripped = line_stripped[1:].strip()
                    if line_stripped and not line_stripped.startswith('**'):
                        precautions.append(line_stripped)
            
            if medications or instructions or precautions:
                sys.stderr.write(f"   → ✅ Parsed {len(medications)} meds, {len(instructions)} instructions, {len(precautions)} precautions\n")
                sys.stderr.flush()
                return {
                    'medications': medications if medications else [{'name': 'Rest', 'dosage': 'As needed', 'frequency': 'Daily', 'duration': '1 week'}],
                    'instructions': instructions if instructions else ['Follow general health guidelines'],
                    'precautions': precautions if precautions else ['Consult doctor if symptoms worsen'],
                    'lifestyle_recommendations': ['Stay hydrated', 'Get adequate rest'],
                    'follow_up': 'Follow up if no improvement in 1 week',
                    'disclaimer': 'AI-generated recommendation. Consult healthcare professional.'
                }
        
        # OLD METHODS: Try JSON extraction
        json_text = None
        
        # Method 1: Check for markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1).strip()
            sys.stderr.write(f"   → Found JSON in markdown block\n")
        
        # Method 2: Find JSON object with balanced braces
        if not json_text:
            # Find outermost { } pair
            start = text.find('{')
            if start != -1:
                brace_count = 0
                for i in range(start, len(text)):
                    if text[i] == '{':
                        brace_count += 1
                    elif text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_text = text[start:i+1]
                            sys.stderr.write(f"   → Found JSON with balanced braces\n")
                            break
        
        # Method 3: Try to parse the whole response
        if not json_text:
            try:
                content = json.loads(text)
                sys.stderr.write(f"   → Entire response is valid JSON\n")
                sys.stderr.flush()
                return AIPrescriptionGenerator()._format_response(content)
            except:
                pass
        
        # If we found JSON text, try to parse it
        if json_text:
            sys.stderr.write(f"   → Extracted JSON: {json_text[:150]}...\n")
            sys.stderr.flush()
            try:
                content = json.loads(json_text)
                sys.stderr.write(f"   → ✅ Successfully parsed LLaMA 3 JSON\n")
                sys.stderr.flush()
                return AIPrescriptionGenerator()._format_response(content)
            except Exception as e:
                sys.stderr.write(f"   → Warning: JSON parse failed: {e}\n")
                sys.stderr.flush()
        
        # If all parsing failed, return error message in structured format
        sys.stderr.write(f"   → ❌ Could not extract valid JSON from response\n")
        sys.stderr.flush()
        return {
            'medications': [{'name': 'Unable to generate', 'dosage': 'N/A', 'frequency': 'N/A', 'duration': 'N/A'}],
            'instructions': [text[:300] if text else 'LLaMA 3 response could not be parsed. Please try again.'],
            'precautions': ['Consult a healthcare professional'],
            'lifestyle_recommendations': ['Seek medical advice'],
            'follow_up': 'Schedule doctor appointment immediately',
            'disclaimer': 'AI generation failed. Professional medical consultation required.'
        }


class HuggingFacePrescriptionGenerator:
    """
    Use HuggingFace models for prescription generation
    Free tier available, can use medical-specific models
    """
    
    def __init__(self):
        """Initialize with HuggingFace API"""
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.use_hf = bool(self.api_key)
        
        if not self.use_hf:
            from models.prescription_generator import PrescriptionGenerator
            self.fallback_generator = PrescriptionGenerator()
    
    
    
    def generate(self, diagnosis: Dict, patient: Dict = None) -> Dict:
        """Generate prescription using LLaMA 3 ONLY - no fallback"""
        import sys
        
        sys.stderr.write("\n" + "="*60 + "\n")
        sys.stderr.write("🤖 USING LLaMA 3 FOR PRESCRIPTION GENERATION\n")
        sys.stderr.write("="*60 + "\n")
        sys.stderr.flush()
        
        try:
            result = self._generate_with_ollama(diagnosis, patient)
            sys.stderr.write("\n✅ LLaMA 3 successfully generated prescription\n\n")
            sys.stderr.flush()
            return result
        except Exception as e:
            sys.stderr.write(f"\n❌ LLaMA 3 FAILED: {e}\n\n")
            sys.stderr.flush()
            raise RuntimeError(f"LLaMA 3 prescription generation failed: {e}. No fallback available.")
