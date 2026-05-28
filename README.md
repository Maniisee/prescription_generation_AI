# AI Disease Detection & Prescription System

**Automated Healthcare Diagnosis System for Rural & Underserved Areas**

## 🎯 Project Overview

An AI-powered healthcare system that identifies diseases based on patient symptoms and vitals, then generates preliminary prescriptions automatically. Designed to provide immediate healthcare support in areas with limited medical access.

## ✨ Features

- **User Authentication**: Secure signup and login system
- **Patient Data Management**: Input and store vitals, symptoms, medical history
- **AI Disease Detection**: ML/DL models for automated diagnosis
- **Prescription Generation**: AI-generated treatment recommendations
- **Web Interface**: User-friendly Bootstrap UI
- **Data Privacy**: HIPAA-compliant secure data handling

## 🏗️ Architecture

```
disease_detection_ai/
├── backend/              # Python Flask API server
│   ├── app.py           # Main Flask application
│   ├── models/          # ML disease detection models
│   ├── routes/          # API endpoints
│   └── utils/           # Helper functions
├── frontend/            # HTML/CSS/JS web interface
│   ├── index.html       # Landing page
│   ├── signup.html      # User registration
│   ├── login.html       # Authentication
│   ├── patient.html     # Patient details form
│   └── prescription.html # AI results display
├── models/              # Trained ML models
├── database/            # MySQL schemas and scripts
└── tests/               # Unit and integration tests
```

## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3, Bootstrap 5
- JavaScript (ES6+)
- AJAX for API calls

**Backend:**
- Python 3.9+
- Flask/FastAPI REST API
- MySQL database

**AI/ML:**
- scikit-learn (Random Forest, SVM)
- pandas, numpy, scipy
- TensorFlow/Keras (optional for deep learning)
- NLP for symptom processing

**Security:**
- bcrypt for password hashing
- JWT for session management
- Input validation and sanitization

## 📋 System Requirements

**Hardware:**
- Processor: Intel Core i5 or higher
- RAM: 8 GB minimum
- Disk: 20 GB free space
- Monitor: 15" color display
- Internet connectivity

**Software:**
- OS: Windows 10+, macOS, or Linux
- Python 3.9+
- MySQL 8.0+
- Web browser (Chrome, Firefox, Safari)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd disease_detection_ai
```

### 2. Setup Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Database
```bash
mysql -u root -p < database/schema.sql
```

Edit `backend/config.py` with your MySQL credentials:
```python
DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'disease_detection'
```

### 4. Train ML Models (Optional)
```bash
python models/train_models.py
```

### 5. Run the Application
```bash
cd backend
python app.py
```

Visit: http://localhost:5000

## 📊 System Modules

### 1. UI Module (Frontend)
- **Sign-Up Page**: New user registration with validation
- **Login Page**: Secure authentication
- **Patient Details Page**: Input vitals (BP, temp, pulse), symptoms, history
- **Prescription Page**: Display AI diagnosis and recommendations

### 2. AI Module (Backend)
- **Input Processing**: Parse symptoms and vitals
- **Disease Prediction**: ML classification models
- **Prescription Generation**: Rule-based + AI recommendations
- **Database Operations**: Store and retrieve patient data

### 3. Database Module
- **Users Table**: Authentication credentials
- **Patients Table**: Medical records
- **Diseases Table**: Disease information
- **Prescriptions Table**: Generated treatments

## 🔬 ML Models

### Disease Classification
- **Algorithm**: Random Forest Classifier
- **Features**: Symptoms (one-hot encoded), vitals (normalized)
- **Output**: Disease prediction with confidence score

### Symptom Analysis
- **NLP Processing**: Keyword extraction, similarity matching
- **Disease Mapping**: Symptom-to-disease correlation matrix

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/
```

## 📸 Screenshots

[Screenshots will be added during implementation]

## 🔒 Security & Privacy

- Password hashing with bcrypt
- SQL injection prevention
- XSS protection
- Data encryption at rest
- HIPAA compliance considerations
- Secure session management

## 🔄 Workflow

1. **Self-Monitoring**: Patient inputs symptoms and vitals
2. **Diagnosis**: AI analyzes data and predicts disease
3. **Treatment Plan**: System generates prescription
4. **Assessment**: Healthcare worker reviews (optional)
5. **Update**: Patient records updated in database

## 📈 Future Enhancements

- Mobile app (iOS/Android)
- Advanced deep learning models
- Integration with medical devices (IoT)
- Telemedicine video consultation
- Multi-language support
- Explainable AI for transparency
- Real-time health monitoring dashboard

## 📚 References

- Healthcare AI research papers
- Medical datasets (MRI, CT, genomics)
- WHO disease classification standards
- Python ML/DL libraries documentation

## 👥 Contributors

- K. Manikandan
- SRM Institute of Science and Technology

## 📄 License

This project is for educational purposes. Medical advice should be verified by licensed healthcare professionals.

## ⚠️ Disclaimer

This system provides preliminary diagnosis only. It is NOT a replacement for professional medical consultation. Always consult with qualified healthcare providers for accurate diagnosis and treatment.

---

**Built with ❤️ for better healthcare accessibility**
