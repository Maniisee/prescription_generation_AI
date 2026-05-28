#!/bin/bash
# Ollama Installation and Setup Script

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🤖 Local AI Setup - Ollama Installation Guide               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed!"
    ollama --version
else
    echo "📦 Ollama is not installed."
    echo ""
    echo "🔽 Installation Steps:"
    echo ""
    echo "1️⃣  Open your browser and go to:"
    echo "    https://ollama.ai/download"
    echo ""
    echo "2️⃣  Click 'Download for macOS'"
    echo ""
    echo "3️⃣  Open the downloaded file and drag Ollama to Applications"
    echo ""
    echo "4️⃣  Open Terminal and run:"
    echo "    ollama --version"
    echo ""
    echo "⏸️  Press ENTER after installing Ollama to continue..."
    read -r
fi

# Check if Ollama is now available
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama still not found. Please:"
    echo "   1. Download from: https://ollama.ai/download"
    echo "   2. Install the app"
    echo "   3. Open Terminal and run: ollama --version"
    echo "   4. Run this script again"
    exit 1
fi

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "  Step 1: Download AI Model"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Available models:"
echo "  • llama3 (4.7GB) - Fast, good quality ⭐⭐⭐⭐"
echo "  • medllama2 (3.8GB) - Medical-specific ⭐⭐⭐⭐"
echo "  • llama3:70b (40GB) - Best quality, slower ⭐⭐⭐⭐⭐"
echo ""
echo "Recommended: llama3 (best balance of speed and quality)"
echo ""

# Check if model is already downloaded
if ollama list | grep -q "llama3"; then
    echo "✅ llama3 model is already installed!"
else
    echo "📥 Downloading llama3 model (this will take 5-10 minutes)..."
    echo ""
    ollama pull llama3
    
    if [ $? -eq 0 ]; then
        echo "✅ Model downloaded successfully!"
    else
        echo "❌ Download failed. Please check your internet connection."
        exit 1
    fi
fi

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "  Step 2: Start Ollama Server"
echo "══════════════════════════════════════════════════════════════════"
echo ""

# Check if Ollama server is running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama server is already running!"
else
    echo "🚀 Starting Ollama server..."
    echo ""
    echo "Opening new terminal window to run Ollama server..."
    echo "(Keep that window open while using the app)"
    echo ""
    
    # Start Ollama in a new terminal window
    osascript -e 'tell app "Terminal" to do script "ollama serve"'
    
    echo "⏳ Waiting for server to start..."
    sleep 3
    
    # Verify server is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama server started successfully!"
    else
        echo "❌ Server failed to start. Please run manually:"
        echo "   ollama serve"
        exit 1
    fi
fi

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "  Step 3: Test AI Model"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Testing AI with a simple medical query..."
echo ""

# Test the model
RESPONSE=$(curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "List 3 common symptoms of flu. Answer in one sentence.",
  "stream": false
}')

if [ $? -eq 0 ]; then
    echo "✅ AI Model Test Successful!"
    echo ""
    echo "AI Response:"
    echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['response'][:200] + '...')" 2>/dev/null || echo "$RESPONSE"
else
    echo "❌ Test failed. Please check if Ollama is running:"
    echo "   curl http://localhost:11434/api/tags"
fi

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "  Step 4: Test with Your Project"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Running prescription generator test..."
echo ""

cd "$(dirname "$0")"
if [ -f "test_ai_generator.py" ]; then
    source venv/bin/activate 2>/dev/null
    python3 test_ai_generator.py
else
    echo "⚠️  Test script not found. Run manually:"
    echo "   cd /Users/manikandank/Downloads/disease_detection_ai"
    echo "   source venv/bin/activate"
    echo "   python test_ai_generator.py"
fi

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "  ✨ Setup Complete!"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Your local AI is ready to use! 🎉"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1️⃣  Update your backend to use local AI:"
echo "    Edit: backend/routes/prescription.py"
echo "    Change line 12 to:"
echo "    from models.ai_prescription_generator import LocalLLMPrescriptionGenerator"
echo "    generator = LocalLLMPrescriptionGenerator()"
echo ""
echo "2️⃣  Restart your backend:"
echo "    lsof -ti:5001 | xargs kill -9"
echo "    cd /Users/manikandank/Downloads/disease_detection_ai"
echo "    source venv/bin/activate"
echo "    python backend/app.py"
echo ""
echo "3️⃣  Test it:"
echo "    Go to: http://localhost:8080/quick_diagnosis.html"
echo "    Create a diagnosis and view prescription"
echo ""
echo "💡 Tips:"
echo "  • Keep Ollama server running (Terminal window)"
echo "  • First prescription takes ~15 seconds (model loading)"
echo "  • Subsequent prescriptions: ~5-10 seconds"
echo "  • 100% free, unlimited usage!"
echo ""
echo "📚 For more info, see: AI_INTEGRATION_GUIDE.md"
echo ""
