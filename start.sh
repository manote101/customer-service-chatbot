#!/bin/bash
# Quick start script for the customer service chatbot

set -e

echo "🚀 Starting Customer Service Chatbot..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Create .env files if they don't exist
echo "1️⃣  Setting up environment files..."
if [ ! -f "backend/.env" ]; then
    echo "   Creating backend/.env from .env.example..."
    cp backend/.env.example backend/.env
fi

if [ ! -f "frontend/.env" ]; then
    echo "   Creating frontend/.env from .env.example..."
    cp frontend/.env.example frontend/.env
fi

# Start PostgreSQL
echo ""
echo "2️⃣  Starting PostgreSQL..."
docker-compose up -d postgres

echo "   Waiting for PostgreSQL to be ready..."
sleep 5

# Check if we should use Docker or local development
if [ "$1" = "--docker" ]; then
    echo ""
    echo "3️⃣  Starting all services with Docker..."
    docker-compose up -d
    
    echo ""
    echo "✅ All services started!"
    echo ""
    echo "📍 Frontend: http://localhost:3000"
    echo "📍 Backend: http://localhost:8000"
    echo "📍 API Docs: http://localhost:8000/docs"
    echo ""
    echo "View logs: docker-compose logs -f"
    echo "Stop all: docker-compose down"
else
    echo ""
    echo "3️⃣  Setting up backend (local development)..."
    cd backend
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        echo "❌ uv is not installed. Please install uv first:"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    echo "   Installing dependencies with uv..."
    uv sync --extra dev --quiet
    
    echo "   Running database migrations..."
    uv run alembic upgrade head
    
    echo "   ✅ Backend ready"
    
    # Setup frontend
    echo ""
    echo "4️⃣  Setting up frontend..."
    cd ../frontend
    
    if [ ! -d "node_modules" ]; then
        echo "   Installing npm dependencies..."
        npm install --silent
    fi
    
    echo "   ✅ Frontend ready"
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "To start the servers:"
    echo ""
    echo "Terminal 1 (Backend):"
    echo "  cd backend"
    echo "  uv run uvicorn app.main:app --reload"
    echo ""
    echo "Terminal 2 (Frontend):"
    echo "  cd frontend"
    echo "  npm start"
    echo ""
    echo "Or run with Docker:"
    echo "  ./start.sh --docker"
fi

echo "   ✅ Frontend ready"

# Start services
echo ""
echo "4️⃣  Starting services..."
echo ""
echo "   Backend will run on: http://localhost:8000"
echo "   Frontend will run on: http://localhost:3000"
echo ""
echo "   Press Ctrl+C to stop all services"
echo ""

cd ..

# Start backend in background
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend in background
cd ../frontend
npm start &
FRONTEND_PID=$!

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait
