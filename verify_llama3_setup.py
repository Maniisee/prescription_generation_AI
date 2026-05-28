#!/usr/bin/env python3
"""
LLaMA 3 Integration Verification Script
Tests all components of the AI integration
"""

import json
import sys
import time
import requests
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

def check_ollama_installed():
    """Check if Ollama is installed"""
    print_header("1. Checking Ollama Installation")
    
    import subprocess
    try:
        result = subprocess.run(['which', 'ollama'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        
        if result.returncode == 0:
            print_success(f"Ollama found at: {result.stdout.strip()}")
            
            # Get version
            version_result = subprocess.run(['ollama', '--version'],
                                          capture_output=True,
                                          text=True,
                                          timeout=5)
            if version_result.returncode == 0:
                print_info(f"Version: {version_result.stdout.strip()}")
            return True
        else:
            print_error("Ollama not found")
            print_info("Install from: https://ollama.ai/download")
            return False
            
    except Exception as e:
        print_error(f"Error checking Ollama: {e}")
        return False

def check_ollama_server():
    """Check if Ollama server is running"""
    print_header("2. Checking Ollama Server")
    
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        
        if response.status_code == 200:
            print_success("Ollama server is running on localhost:11434")
            
            data = response.json()
            models = data.get('models', [])
            
            if models:
                print_info(f"Available models: {len(models)}")
                for model in models:
                    name = model.get('name', 'unknown')
                    size_gb = model.get('size', 0) / (1024**3)
                    print(f"   • {name} ({size_gb:.1f} GB)")
            else:
                print_warning("No models downloaded yet")
                
            return True
        else:
            print_error(f"Server responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to Ollama server")
        print_info("Start with: ollama serve")
        return False
    except Exception as e:
        print_error(f"Error checking server: {e}")
        return False

def check_llama3_model():
    """Check if LLaMA 3 model is downloaded"""
    print_header("3. Checking LLaMA 3 Model")
    
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            llama3_found = any('llama3' in model.get('name', '') for model in models)
            
            if llama3_found:
                print_success("LLaMA 3 model is downloaded")
                for model in models:
                    if 'llama3' in model.get('name', ''):
                        size_gb = model.get('size', 0) / (1024**3)
                        print_info(f"Model: {model.get('name')} ({size_gb:.2f} GB)")
                return True
            else:
                print_error("LLaMA 3 model not found")
                print_info("Download with: ollama pull llama3")
                return False
        else:
            print_error("Cannot check models")
            return False
            
    except Exception as e:
        print_error(f"Error checking model: {e}")
        return False

def test_llama3_generation():
    """Test LLaMA 3 generation"""
    print_header("4. Testing LLaMA 3 Generation")
    
    test_prompt = "List 3 common symptoms of flu in one sentence."
    
    print_info("Sending test prompt to LLaMA 3...")
    print(f"   Prompt: {test_prompt}")
    
    try:
        start_time = time.time()
        
        response = requests.post('http://localhost:11434/api/generate',
                                json={
                                    'model': 'llama3',
                                    'prompt': test_prompt,
                                    'stream': False
                                },
                                timeout=60)
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('response', '')
            
            if ai_response:
                print_success(f"Generation successful! ({elapsed:.1f} seconds)")
                print(f"\n{BOLD}AI Response:{RESET}")
                print(f"   {ai_response[:200]}")
                if len(ai_response) > 200:
                    print(f"   ... (truncated)")
                return True
            else:
                print_error("Empty response from model")
                return False
        else:
            print_error(f"Generation failed with status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Request timed out (>60 seconds)")
        print_info("First generation may take longer as model loads into RAM")
        return False
    except Exception as e:
        print_error(f"Error during generation: {e}")
        return False

def check_backend_running():
    """Check if Flask backend is running"""
    print_header("5. Checking Backend Server")
    
    try:
        response = requests.get('http://127.0.0.1:5001/', timeout=5)
        
        if response.status_code == 200:
            print_success("Backend is running on 127.0.0.1:5001")
            return True
        else:
            print_warning(f"Backend responded with status {response.status_code}")
            return True  # Still running, just unexpected response
            
    except requests.exceptions.ConnectionError:
        print_error("Backend is not running")
        print_info("Start with: python backend/app.py")
        return False
    except Exception as e:
        print_error(f"Error checking backend: {e}")
        return False

def check_ai_integration_files():
    """Check if AI integration files exist"""
    print_header("6. Checking AI Integration Files")
    
    base_path = Path(__file__).parent
    
    files_to_check = {
        'models/ai_prescription_generator.py': 'AI Generator (main integration)',
        'backend/routes/prescription.py': 'Prescription routes',
        'AI_INTEGRATION_GUIDE.md': 'Integration guide',
        'test_ai_generator.py': 'Test script',
        'SETUP_LLAMA3.sh': 'Setup script',
        'QUICK_START.md': 'Quick start guide'
    }
    
    all_found = True
    
    for file_path, description in files_to_check.items():
        full_path = base_path / file_path
        
        if full_path.exists():
            size_kb = full_path.stat().st_size / 1024
            print_success(f"{description}: {file_path} ({size_kb:.1f} KB)")
        else:
            print_error(f"{description}: {file_path} - NOT FOUND")
            all_found = False
    
    return all_found

def test_prescription_endpoint():
    """Test the prescription endpoint with AI"""
    print_header("7. Testing Prescription Endpoint")
    
    # First need to login
    print_info("Logging in...")
    
    try:
        login_response = requests.post(
            'http://127.0.0.1:5001/api/login',
            json={
                'email': 'test@example.com',
                'password': 'test1234'
            },
            timeout=10
        )
        
        if login_response.status_code != 200:
            print_error("Login failed")
            print_info("Ensure test user exists in database")
            return False
        
        token = login_response.json().get('access_token')
        print_success("Login successful")
        
        # Now test prescription generation
        print_info("Generating AI-powered prescription...")
        
        test_diagnosis = {
            'disease': 'Common Cold',
            'confidence': 92.5,
            'matched_symptoms': ['Cough', 'Fever', 'Headache'],
            'vitals': {
                'blood_pressure_systolic': 120,
                'blood_pressure_diastolic': 80,
                'temperature': 100.5,
                'pulse': 82
            }
        }
        
        test_patient = {
            'age': 35,
            'gender': 'Male',
            'medical_history': 'None'
        }
        
        start_time = time.time()
        
        prescription_response = requests.post(
            'http://127.0.0.1:5001/api/prescriptions',
            json={
                'diagnosis_id': 1,  # Using existing diagnosis
                'patient_id': 1
            },
            headers={'Authorization': f'Bearer {token}'},
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if prescription_response.status_code == 200 or prescription_response.status_code == 201:
            data = prescription_response.json()
            
            print_success(f"Prescription generated! ({elapsed:.1f} seconds)")
            
            prescription = data.get('prescription', {})
            
            # Check if it's AI-generated
            medications = prescription.get('medications', [])
            instructions = prescription.get('instructions', '')
            
            print(f"\n{BOLD}Sample Prescription:{RESET}")
            print(f"   Disease: {prescription.get('disease_name', 'N/A')}")
            print(f"   Medications: {len(medications)} items")
            
            if medications:
                print(f"   • {medications[0].get('name', 'N/A')}")
            
            if instructions and len(instructions) > 50:
                print_info("Instructions contain detailed AI-generated content")
            else:
                print_warning("Instructions seem short (might be rule-based)")
            
            return True
        else:
            print_error(f"Prescription failed with status {prescription_response.status_code}")
            print(f"   Response: {prescription_response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Error testing endpoint: {e}")
        return False

def print_summary(results):
    """Print final summary"""
    print_header("Summary")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n{BOLD}Tests Passed: {passed}/{total}{RESET}\n")
    
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        color = GREEN if result else RED
        print(f"{color}{status}{RESET} - {check}")
    
    print("\n")
    
    if passed == total:
        print(f"{GREEN}{BOLD}🎉 All checks passed! LLaMA 3 integration is working!{RESET}\n")
        print("Next steps:")
        print("  1. Visit: http://localhost:8080/quick_diagnosis.html")
        print("  2. Login: test@example.com / test1234")
        print("  3. Generate AI-powered prescriptions!")
    elif passed >= total - 2:
        print(f"{YELLOW}{BOLD}⚠️  Almost ready! Fix the failed checks above.{RESET}\n")
    else:
        print(f"{RED}{BOLD}❌ Setup incomplete. Please address the failed checks.{RESET}\n")
        print("Quick fixes:")
        if not results.get('Ollama Installed'):
            print("  • Install Ollama: https://ollama.ai/download")
        if not results.get('Ollama Server'):
            print("  • Start server: ollama serve")
        if not results.get('LLaMA 3 Model'):
            print("  • Download model: ollama pull llama3")
        if not results.get('Backend Running'):
            print("  • Start backend: python backend/app.py")
        print()

def main():
    print(f"\n{BOLD}{BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║        LLaMA 3 Integration Verification Script                       ║")
    print("║        Disease Detection AI - Component Testing                      ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")
    
    print_info("This script will verify your LLaMA 3 integration setup")
    print_info("Testing all components...\n")
    
    time.sleep(1)
    
    # Run all checks
    results = {}
    
    results['Ollama Installed'] = check_ollama_installed()
    results['Ollama Server'] = check_ollama_server()
    
    if results['Ollama Server']:
        results['LLaMA 3 Model'] = check_llama3_model()
        
        if results['LLaMA 3 Model']:
            results['AI Generation'] = test_llama3_generation()
        else:
            print_warning("Skipping generation test (model not downloaded)")
            results['AI Generation'] = False
    else:
        print_warning("Skipping model checks (server not running)")
        results['LLaMA 3 Model'] = False
        results['AI Generation'] = False
    
    results['Backend Running'] = check_backend_running()
    results['Integration Files'] = check_ai_integration_files()
    
    if results['Backend Running'] and results['Ollama Server']:
        results['Prescription Endpoint'] = test_prescription_endpoint()
    else:
        print_warning("Skipping endpoint test (prerequisites not met)")
        results['Prescription Endpoint'] = False
    
    # Print summary
    print_summary(results)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Test interrupted by user{RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{RED}❌ Unexpected error: {e}{RESET}\n")
        sys.exit(1)
