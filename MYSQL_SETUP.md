# MySQL Setup Instructions

## Option 1: Install MySQL (Recommended for Production)

### For macOS:
```bash
# Using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation
mysql_secure_installation

# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE disease_detection;

# Import schema
mysql -u root -p disease_detection < database/schema.sql

# Verify
mysql -u root -p -e "USE disease_detection; SHOW TABLES;"
```

### Update .env file:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=disease_detection
```

## Option 2: Quick Test Without MySQL

For quick testing, you can modify the application to use an in-memory dictionary instead of MySQL.

### Quick Start Instructions:

1. **Update the .env file** with your MySQL credentials (or keep defaults for now)

2. **Start the Flask Backend:**
   ```bash
   cd /Users/manikandank/Downloads/disease_detection_ai
   source venv/bin/activate
   python backend/app.py
   ```
   
   The server will start on http://localhost:5000

3. **Open the Frontend:**
   - Option A: Open directly in browser
     ```bash
     open frontend/index.html
     ```
   
   - Option B: Use Python HTTP server (recommended to avoid CORS issues)
     ```bash
     cd frontend
     python3 -m http.server 8080
     ```
     Then open http://localhost:8080 in your browser

4. **Test the Application:**
   - Click "Sign Up" and create an account
   - Login with your credentials
   - Fill in patient details with symptoms
   - View AI diagnosis and prescription

## Testing Without Database (Development Mode)

If you want to test immediately without MySQL, you can modify `database/db_manager.py` to use temporary in-memory storage. This is NOT recommended for production but useful for quick testing.

## Current Status:
- ✅ All Python dependencies installed
- ✅ Virtual environment created
- ✅ Frontend pages complete
- ✅ Backend API ready
- ⏳ MySQL installation needed
- ⏳ Database schema import pending

## Next Steps:
1. Install MySQL using Homebrew: `brew install mysql`
2. Start MySQL service: `brew services start mysql`
3. Create database and import schema
4. Update .env with actual credentials
5. Start Flask backend: `python backend/app.py`
6. Open frontend in browser
7. Test complete workflow

## Troubleshooting:
- **Port 5000 already in use**: Change FLASK_RUN_PORT in .env or kill the process using `lsof -ti:5000 | xargs kill -9`
- **MySQL connection error**: Verify MySQL is running with `brew services list`
- **CORS errors**: Use Python HTTP server for frontend instead of file:// protocol
- **Module not found**: Ensure virtual environment is activated with `source venv/bin/activate`
