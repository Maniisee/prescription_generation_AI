#!/bin/bash

echo "======================================"
echo "  AI Disease Detection System"
echo "  Starting Servers..."
echo "======================================"
echo ""

# Navigate to project directory
cd /Users/manikandank/Downloads/disease_detection_ai

# Kill existing processes
echo "1. Cleaning up old processes..."
pkill -9 -f "backend/app.py" 2>/dev/null
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null
sleep 2
echo "   ✓ Cleanup complete"
echo ""

# Start Backend
echo "2. Starting Backend API..."
nohup ./venv/bin/python backend/app.py > backend.log 2>&1 &
BACKEND_PID=$!
sleep 4

# Test backend
if curl -s http://localhost:5001/ > /dev/null 2>&1; then
    echo "   ✓ Backend running (PID: $BACKEND_PID) on http://localhost:5001"
else
    echo "   ✗ Backend failed to start!"
    echo "   Check backend.log for errors:"
    tail -20 backend.log
    exit 1
fi
echo ""

# Start Frontend
echo "3. Starting Frontend..."
cd frontend
nohup python3 -m http.server 8080 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 2

# Test frontend
if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    echo "   ✓ Frontend running (PID: $FRONTEND_PID) on http://localhost:8080"
else
    echo "   ✗ Frontend failed to start!"
    exit 1
fi
echo ""

# Test login
echo "4. Testing Login API..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test1234"}' 2>&1)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✓ Login API working"
else
    echo "   ✗ Login API failed (HTTP $HTTP_CODE)"
fi
echo ""

echo "======================================"
echo "  ✅ SYSTEM IS READY!"
echo "======================================"
echo ""
echo "📍 Access the application:"
echo "   • Main Login:   http://localhost:8080/login.html"
echo "   • Simple Login: http://localhost:8080/simple_login.html"
echo "   • Patient Page: http://localhost:8080/patient.html"
echo ""
echo "🔑 Login Credentials:"
echo "   Email:    test@example.com"
echo "   Password: test1234"
echo ""
echo "🛠️  Management:"
echo "   Stop servers:  pkill -f backend/app.py && lsof -ti:8080 | xargs kill"
echo "   View logs:     tail -f backend.log"
echo "   Restart:       $0"
echo ""
echo "======================================"
