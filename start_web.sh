#!/bin/bash

echo "🎸 GuitarHarmony Web Interface Launcher"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed or not in PATH"
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed or not in PATH"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    pkill -f "python api_server.py"
    pkill -f "npm start"
    echo "👋 Goodbye!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "🚀 Starting API server..."
python api_server.py &
API_PID=$!

echo "⏳ Waiting for API server to start..."
sleep 3

# Check if API server is running
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ API server is running on http://localhost:8000"
else
    echo "❌ Failed to start API server"
    exit 1
fi

echo ""
echo "🚀 Starting React development server..."
cd guitar-harmony-web
npm start &
REACT_PID=$!

echo "⏳ Waiting for React server to start..."
sleep 5

# Check if React server is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ React server is running on http://localhost:3000"
else
    echo "❌ Failed to start React server"
    exit 1
fi

echo ""
echo "🎉 Both servers are running!"
echo "📱 Open your browser and go to: http://localhost:3000"
echo "📚 API documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user to stop
wait 