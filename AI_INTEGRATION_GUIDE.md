# AI Model Integration Guide

## 🤖 Options for AI-Powered Prescriptions

### **Option 1: OpenAI GPT (Recommended)**
**Pros:** Best quality, most reliable, easy to use
**Cons:** Requires API key ($), costs per request (~$0.01-0.03 per prescription)

#### Setup:
```bash
# 1. Install OpenAI package
cd /Users/manikandank/Downloads/disease_detection_ai
source venv/bin/activate
pip install openai

# 2. Get API key from https://platform.openai.com/api-keys

# 3. Add to .env file
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# 4. Update backend to use AI generator
```

**Update backend/routes/prescription.py:**
```python
# Change line 12 from:
from models.prescription_generator import PrescriptionGenerator
generator = PrescriptionGenerator()

# To:
from models.ai_prescription_generator import AIPrescriptionGenerator
generator = AIPrescriptionGenerator()
```

**Cost:** ~$0.01-0.03 per prescription with GPT-4, ~$0.001 with GPT-3.5-turbo

---

### **Option 2: Local LLM with Ollama (FREE)**
**Pros:** 100% free, runs offline, no API limits, privacy
**Cons:** Requires powerful computer (16GB+ RAM), slower

#### Setup:
```bash
# 1. Install Ollama
# Visit https://ollama.ai and download for Mac

# 2. Pull medical model
ollama pull llama3
# or
ollama pull medllama2

# 3. Start Ollama (runs in background)
ollama serve

# 4. Install Python package
pip install requests

# 5. Update backend
```

**Update backend/routes/prescription.py:**
```python
from models.ai_prescription_generator import LocalLLMPrescriptionGenerator
generator = LocalLLMPrescriptionGenerator(model_name="llama3")
```

---

### **Option 3: HuggingFace (FREE Tier Available)**
**Pros:** Free tier, many medical models, no local resources needed
**Cons:** Rate limits on free tier, slower than OpenAI

#### Setup:
```bash
# 1. Get API key from https://huggingface.co/settings/tokens

# 2. Add to .env
echo "HUGGINGFACE_API_KEY=hf_your-key-here" >> .env

# 3. Update backend
```

**Update backend/routes/prescription.py:**
```python
from models.ai_prescription_generator import HuggingFacePrescriptionGenerator
generator = HuggingFacePrescriptionGenerator()
```

---

### **Option 4: Hybrid (Recommended for Production)**
**Pros:** Safe rule-based + AI personalization, best of both worlds
**Cons:** Still needs AI API

Combines validated medical protocols with personalized AI advice.

```python
from models.ai_prescription_generator import HybridPrescriptionGenerator
generator = HybridPrescriptionGenerator()
```

---

## 🚀 Quick Start (OpenAI)

```bash
# 1. Install package
cd /Users/manikandank/Downloads/disease_detection_ai
source venv/bin/activate
pip install openai python-dotenv

# 2. Create .env file with API key
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-key-here
SECRET_KEY=your-flask-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=disease_detection
EOF

# 3. Test AI generator
python -c "
from models.ai_prescription_generator import AIPrescriptionGenerator
gen = AIPrescriptionGenerator()
result = gen.generate(
    {'disease': 'Flu', 'confidence': 85, 'severity': 'medium', 'matched_symptoms': ['fever', 'cough']},
    {'age': 35, 'gender': 'male', 'medical_history': 'None'}
)
print(result)
"
```

---

## 🔧 Implementation Steps

### **Step 1: Choose Your Option**
Pick one: OpenAI (easiest), Ollama (free but local), HuggingFace (free but limited)

### **Step 2: Install Dependencies**
```bash
# For OpenAI:
pip install openai python-dotenv

# For Ollama:
pip install requests
# + Download Ollama app

# For HuggingFace:
pip install requests python-dotenv
```

### **Step 3: Update Backend**
Edit `/Users/manikandank/Downloads/disease_detection_ai/backend/routes/prescription.py`

Change the import at the top:
```python
# OLD:
from models.prescription_generator import PrescriptionGenerator
generator = PrescriptionGenerator()

# NEW (pick one):
from models.ai_prescription_generator import AIPrescriptionGenerator
generator = AIPrescriptionGenerator()  # OpenAI

# OR:
from models.ai_prescription_generator import LocalLLMPrescriptionGenerator
generator = LocalLLMPrescriptionGenerator()  # Ollama

# OR:
from models.ai_prescription_generator import HybridPrescriptionGenerator
generator = HybridPrescriptionGenerator()  # Best of both
```

### **Step 4: Restart Backend**
```bash
# Kill old backend
lsof -ti:5001 | xargs kill -9

# Start new backend
cd /Users/manikandank/Downloads/disease_detection_ai
source venv/bin/activate
python backend/app.py
```

### **Step 5: Test**
Go to http://localhost:8080/quick_diagnosis.html and create a diagnosis.
The prescription will now be AI-generated!

---

## 💡 Comparison Table

| Feature | OpenAI GPT | Ollama (Local) | HuggingFace | Rule-Based (Current) |
|---------|-----------|----------------|-------------|---------------------|
| **Cost** | $0.01-0.03/rx | FREE | FREE (limited) | FREE |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | Fast (1-3s) | Medium (5-10s) | Medium (3-5s) | Instant |
| **Personalization** | Excellent | Good | Good | Basic |
| **Privacy** | Cloud | Local | Cloud | Local |
| **Setup** | Easy | Medium | Easy | Done ✅ |
| **Reliability** | Very High | High | Medium | Very High |

---

## ⚠️ Important Notes

1. **Medical Disclaimer:** AI-generated prescriptions should be reviewed by licensed medical professionals
2. **Fallback:** All AI generators automatically fallback to rule-based if AI fails
3. **API Keys:** Never commit API keys to Git. Always use .env files
4. **Testing:** Test thoroughly before production use
5. **Monitoring:** Monitor API costs if using paid services

---

## 🎯 My Recommendation

**For Development/Testing:** Use **Ollama** (free, runs locally)
**For Production:** Use **Hybrid** (safe + personalized) with OpenAI GPT-3.5-turbo (cheaper)

The Hybrid approach gives you:
- ✅ Validated medical protocols (rule-based core)
- ✅ Personalized lifestyle advice (AI enhancement)
- ✅ Safety (falls back if AI fails)
- ✅ Cost-effective (only enhances, doesn't replace)
