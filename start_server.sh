#!/bin/bash

# Start Backend and Frontend Servers for Disease Detection AI

echo "🚀 Starting AI Disease Detection System..."

# Kill any existing processes
echo "Cleaning up old processes..."
pkill -9 -f "backend/app.py" 2>/dev/null
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null
sleep 2

# Navigate to project directory
cd /Users/manikandank/Downloads/disease_detection_ai

# Start Backend
echo "Starting Backend API (Port 5001)..."
PYTHONPATH=/Users/manikandank/Downloads/disease_detection_ai \
    ./venv/bin/python backend/app.py > backend.log 2>&1 &
BACKEND_PID=$!

sleep 3

# Check if backend started
if curl -s http://localhost:5001/ > /dev/null 2>&1; then
    echo "✅ Backend API is running (PID: $BACKEND_PID)"
else
    echo "❌ Backend failed to start. Check backend.log"
    cat backend.log
    exit 1
fi

# Start Frontend
echo "Starting Frontend (Port 8080)..."
cd frontend
python3 -m http.server 8080 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

sleep 2

# Check if frontend started
if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    echo "✅ Frontend is running (PID: $FRONTEND_PID)"
else
    echo "❌ Frontend failed to start"
    exit 1
fi

echo ""
echo "🎉 System is ready!"
echo "================================"
echo "Backend API:  http://localhost:5001"
echo "Frontend App: http://localhost:8080"
echo "Login Page:   http://localhost:8080/login.html"
echo ""
echo "Test Credentials:"
echo "  Email:    test@example.com"
echo "  Password: test1234"
echo "================================"
echo ""
echo "To stop the servers, run:"
echo "  pkill -f 'backend/app.py' && lsof -ti:8080 | xargs kill"
