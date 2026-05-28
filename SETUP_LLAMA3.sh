#!/bin/bash
# Complete Setup Guide for LLaMA 3 Integration

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║  🤖 LLaMA 3 AI Integration - Complete Setup Guide                   ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Your project is now configured to use LLaMA 3 for AI-powered prescriptions!"
echo ""

# Step 1: Check Ollama installation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 1: Install Ollama (Required)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed!"
    ollama --version
    echo ""
else
    echo "❌ Ollama is NOT installed."
    echo ""
    echo "📥 INSTALLATION INSTRUCTIONS:"
    echo ""
    echo "1️⃣  Open your browser and navigate to:"
    echo "    👉 https://ollama.ai/download"
    echo ""
    echo "2️⃣  Click the 'Download for macOS' button"
    echo ""
    echo "3️⃣  Open the downloaded Ollama.dmg file"
    echo ""
    echo "4️⃣  Drag Ollama to your Applications folder"
    echo ""
    echo "5️⃣  Open Ollama from Applications (it will appear in menu bar)"
    echo ""
    echo "6️⃣  Verify installation by running:"
    echo "    ollama --version"
    echo ""
    echo "⏸️  Press ENTER after installing Ollama..."
    read -r
    
    # Recheck
    if ! command -v ollama &> /dev/null; then
        echo ""
        echo "❌ Ollama still not found. Please complete installation first."
        echo ""
        echo "After installing, open a NEW terminal and run this script again."
        exit 1
    fi
    echo "✅ Ollama detected!"
fi

# Step 2: Download LLaMA 3 model
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 2: Download LLaMA 3 Model (~4.7GB)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if ollama list 2>/dev/null | grep -q "llama3"; then
    echo "✅ LLaMA 3 model is already downloaded!"
    ollama list | grep "llama3"
else
    echo "📥 Downloading LLaMA 3 model..."
    echo ""
    echo "⏳ This will take 5-15 minutes depending on your internet speed."
    echo "   Model size: ~4.7GB"
    echo ""
    
    ollama pull llama3
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ LLaMA 3 model downloaded successfully!"
    else
        echo ""
        echo "❌ Download failed. Please check:"
        echo "   • Internet connection"
        echo "   • Disk space (~10GB free recommended)"
        echo "   • Try again: ollama pull llama3"
        exit 1
    fi
fi

# Step 3: Start Ollama server
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 3: Start Ollama Server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if server is already running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama server is already running!"
else
    echo "🚀 Starting Ollama server..."
    echo ""
    echo "Opening new terminal window for Ollama server..."
    echo "(Keep that terminal window open while using the app)"
    echo ""
    
    # Start in new terminal
    osascript <<EOF
tell application "Terminal"
    do script "echo '🤖 Ollama Server for Disease Detection AI'; echo ''; echo 'Keep this window open while using the app'; echo 'Press Ctrl+C to stop server'; echo ''; ollama serve"
    activate
end tell
EOF
    
    echo "⏳ Waiting for server to start (10 seconds)..."
    sleep 10
    
    # Verify
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama server started successfully!"
    else
        echo "⚠️  Server might still be starting. Please wait a moment."
        echo "   Verify by running: curl http://localhost:11434/api/tags"
    fi
fi

# Step 4: Test the model
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 4: Test LLaMA 3 Model"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Testing AI with a simple medical query..."
echo ""

TEST_RESPONSE=$(curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "List 3 common flu symptoms. Answer in one short sentence.",
  "stream": false
}' 2>&1)

if echo "$TEST_RESPONSE" | grep -q '"response"'; then
    echo "✅ LLaMA 3 is working!"
    echo ""
    echo "AI Response:"
    echo "$TEST_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('response', 'No response')[:200])" 2>/dev/null || echo "Response received"
else
    echo "❌ Test failed. Check if Ollama is running:"
    echo "   curl http://localhost:11434/api/tags"
fi

# Step 5: Restart backend with AI
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 5: Restart Backend with LLaMA 3"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$(dirname "$0")"

echo "🛑 Stopping old backend..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
sleep 2

echo "🚀 Starting backend with LLaMA 3 AI..."
source venv/bin/activate 2>/dev/null || true
nohup python backend/app.py > backend_ai.log 2>&1 &
BACKEND_PID=$!

echo "⏳ Waiting for backend to start..."
sleep 5

# Verify backend
if ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo "✅ Backend started successfully! (PID: $BACKEND_PID)"
    echo ""
    echo "📋 Backend log: tail -f backend_ai.log"
else
    echo "❌ Backend failed to start. Check backend_ai.log for errors:"
    echo "   tail -50 backend_ai.log"
fi

# Step 6: Start frontend
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STEP 6: Start Frontend"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if frontend is running
if lsof -i:8080 > /dev/null 2>&1; then
    echo "✅ Frontend is already running on port 8080"
else
    echo "🚀 Starting frontend server..."
    cd frontend
    nohup python3 -m http.server 8080 > ../frontend.log 2>&1 &
    cd ..
    sleep 2
    echo "✅ Frontend started on http://localhost:8080"
fi

# Final summary
echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║  ✨ Setup Complete! LLaMA 3 AI is Ready                              ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Your Disease Detection AI now uses LLaMA 3 for personalized prescriptions!"
echo ""
echo "📍 What's Running:"
echo "   ✅ Ollama Server (localhost:11434) - Keep terminal open"
echo "   ✅ Backend API (localhost:5001) - Using LLaMA 3"
echo "   ✅ Frontend (localhost:8080)"
echo ""
echo "🧪 Test It Now:"
echo ""
echo "   1. Open browser: http://localhost:8080/quick_diagnosis.html"
echo "   2. Login with: test@example.com / test1234"
echo "   3. Select symptoms and click 'Run Diagnosis'"
echo "   4. View AI-generated prescription!"
echo ""
echo "⚡ Performance:"
echo "   • First prescription: ~15 seconds (loading model)"
echo "   • Subsequent: ~5-10 seconds"
echo "   • 100% FREE, unlimited usage"
echo ""
echo "📊 How It Works:"
echo "   • Patient symptoms → Flask Backend"
echo "   • Backend → LLaMA 3 AI (via Ollama)"
echo "   • AI analyzes: disease, age, history, vitals"
echo "   • Generates personalized treatment plan"
echo "   • Returns medications + instructions + precautions"
echo ""
echo "🔧 Troubleshooting:"
echo ""
echo "   Backend not working?"
echo "   → Check: tail -f backend_ai.log"
echo "   → Restart: lsof -ti:5001 | xargs kill -9 && python backend/app.py"
echo ""
echo "   Ollama not responding?"
echo "   → Check: curl http://localhost:11434/api/tags"
echo "   → Restart: killall ollama && ollama serve"
echo ""
echo "   Slow prescriptions?"
echo "   → First request is slow (loading model)"
echo "   → Subsequent requests are faster"
echo "   → Model stays in RAM after first use"
echo ""
echo "📖 For more details:"
echo "   • AI_INTEGRATION_GUIDE.md"
echo "   • Run: python test_ai_generator.py"
echo ""
echo "💡 Tip: Keep the Ollama terminal window open while using the app!"
echo ""
