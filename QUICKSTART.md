# Quick Start Guide - AI Disease Detection System

## 🚀 Setup Instructions

### 1. Navigate to Project
```bash
cd /Users/manikandank/Downloads/disease_detection_ai
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database
```bash
# Start MySQL
mysql -u root -p

# Run schema
mysql -u root -p < database/schema.sql
```

### 5. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your MySQL credentials
nano .env
```

### 6. Run the Application
```bash
cd backend
python app.py
```

The API server will start on http://localhost:5000

### 7. Access Frontend
Open `frontend/index.html` in your browser or use a local server:
```bash
cd frontend
python -m http.server 8080
```

Then visit: http://localhost:8080

## 📝 API Endpoints

**Authentication:**
- POST `/api/auth/signup` - Register new user
- POST `/api/auth/login` - Login and get JWT token
- GET `/api/auth/verify` - Verify token

**Patient:**
- POST `/api/patient/create` - Create patient record
- GET `/api/patient/get/<id>` - Get patient details
- GET `/api/patient/history` - Get patient history

**Diagnosis:**
- POST `/api/diagnosis/predict` - Predict disease
- GET `/api/diagnosis/history/<patient_id>` - Get diagnosis history

**Prescription:**
- POST `/api/prescription/generate` - Generate prescription
- GET `/api/prescription/get/<id>` - Get prescription
- GET `/api/prescription/patient/<patient_id>` - Get all prescriptions

## 🧪 Testing

### Test API with curl:
```bash
# Signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 📚 Next Steps

1. Complete the frontend pages (signup.html, login.html, patient.html, prescription.html)
2. Add JavaScript for API integration
3. Implement form validation
4. Add CSS styling
5. Test end-to-end workflow
6. Deploy to production server

## ⚠️ Important Notes

- This is a prototype for educational purposes
- Always consult healthcare professionals for medical advice
- Ensure HIPAA compliance before production use
- Add proper authentication and security measures
- Test thoroughly with real medical data

## 🆘 Troubleshooting

**Database Connection Error:**
- Check MySQL is running
- Verify credentials in .env file
- Ensure database exists

**Import Errors:**
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

**Port Already in Use:**
- Change port in app.py
- Or kill process: `lsof -ti:5000 | xargs kill`

## 📞 Support

For issues or questions, please refer to the main README.md file.
