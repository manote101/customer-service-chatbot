#!/bin/bash
# Simple local development startup

echo "🚀 Starting Customer Service Chatbot (Local Development)"
echo ""

# 1. Start PostgreSQL
echo "Starting PostgreSQL..."
docker-compose up -d postgres
sleep 3

# 2. Backend setup and start
echo ""
echo "Starting Backend..."
cd backend

# Create .env if needed
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# Run migrations
uv run alembic upgrade head 2>/dev/null || echo "Migration skipped (run manually if needed)"

# Start backend in background
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# 3. Frontend setup and start
echo ""
echo "Starting Frontend..."
cd frontend

# Create .env if needed
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# Install deps if needed
if [ ! -d "node_modules" ]; then
    npm install
fi

# Start frontend
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Services started!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Handle Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; docker-compose stop postgres; exit" INT

# Wait
wait
