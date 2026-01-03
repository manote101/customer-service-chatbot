# Customer Service Chatbot

## Project Overview
A web-based customer service chatbot built with React (frontend) and FastAPI (backend). The MVP includes:
- Natural language FAQ responses
- Intent detection (order tracking, returns, escalation)
- Session-based conversation tracking
- Database persistence (PostgreSQL)
- Human agent escalation

## Features

### MVP Features (Implemented)
✅ Basic chat interface with message bubbles  
✅ Message sending/receiving with real-time responses  
✅ Simple intent recognition (order tracking, returns, agent escalation)  
✅ FAQ/policy answers from curated knowledge base  
✅ Clarifying questions for missing details  
✅ Human handoff path with transcript tracking  
✅ Conversation session tracking (session_id)  
✅ Basic safety/privacy handling (PII warnings)  
✅ Health endpoint and operational logging  

## Technology Stack
- **Frontend:** React 18 with TypeScript, Tailwind CSS
- **Backend:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 15
- **Dependency Management:** uv (backend), npm (frontend)

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- [uv](https://github.com/astral-sh/uv) (for Python dependency management)

## Quick Start

### Option 1: Local Development (Recommended)

**Prerequisites:** Docker, Python 3.11+, Node.js 18+, [uv](https://github.com/astral-sh/uv)

```bash
# One-command setup and start
./start.sh

# Then in two separate terminals:

# Terminal 1 - Backend
cd backend
uv run uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm start
```

### Option 2: Full Docker Deployment

```bash
# Build and start all services
./start.sh --docker

# Or manually:
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

### Option 3: Step-by-Step Manual Setup

Start PostgreSQL (using Docker):
```bash
docker-compose up -d postgres
```

Or use local PostgreSQL and create the database:
```bash
createdb chatbot_db
```

#### 2. Backend Setup

```bash
cd backend

# Install dependencies with uv
uv sync --extra dev

# Run database migration
uv run alembic upgrade head

# Start the backend server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## Backend Development (uv)

The backend uses `uv` for dependency management.

- Install dependencies:
  - `cd backend`
  - `uv sync`
  - (dev/test deps) `uv sync --extra dev`
- Run the API locally:
  - `cd backend`
  - `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Run tests:
  - `cd backend`
  - `uv run pytest -q`
- Create a new migration:
  - `uv run alembic revision --autogenerate -m "description"`
- Apply migrations:
  - `uv run alembic upgrade head`

## Testing

### Backend Tests
```bash
cd backend
uv run pytest -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## API Endpoints

### System
- `GET /` - Welcome message
- `GET /health` - Health check

### Chat
- `POST /api/v1/chat` - Send a message and get bot response
  - Request: `{ "message": "string", "session_id": "string?" }`
  - Response: `{ "session_id": "string", "reply": "string", "messages": [...], "handoff": {...}? }`

Full API documentation: `http://localhost:8000/docs`

## Project Structure

```
backend/
  app/
    main.py           # FastAPI app and endpoints
    models.py         # SQLAlchemy database models
    database.py       # Database connection
    knowledge.py      # FAQ knowledge base and intent detection
  alembic/            # Database migrations
  tests/              # Backend tests

frontend/
  src/
    api/
      client.ts       # API client
    components/       # Reusable UI components
      MessageBubble.tsx
      ChatInput.tsx
      TypingIndicator.tsx
      QuickReplies.tsx
    hooks/
      useChat.ts      # Chat state management hook
    pages/
      ChatPage.tsx    # Main chat page
    App.tsx           # Root component

docs/
  api-specification.yaml    # OpenAPI spec
  database-schema.md        # Database design
  project-spec.md           # Project charter
  user-stories.md           # User stories
  prioritization.md         # Feature prioritization
```

## Environment Variables

### Backend
Create `backend/.env`:
```
DATABASE_URL=postgresql://chatbot_user:chatbot_password@localhost:5432/chatbot_db
```

### Frontend
Create `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:8000
```

## Docker Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Knowledge Base

The MVP uses a simple in-memory FAQ system in `backend/app/knowledge.py`. To add or update FAQs:

1. Edit `backend/app/knowledge.py`
2. Add new `FAQ` entries to the `FAQS` list
3. Restart the backend server

For production, replace with:
- Vector database (Pinecone, Weaviate)
- Full-text search (Elasticsearch)
- External knowledge API

## Next Steps (Post-MVP)

See [docs/prioritization.md](docs/prioritization.md) for the full roadmap:

- **Phase 1 (Should Have):**
  - File attachments
  - Conversation history view
  - Analytics dashboard
  - CSAT feedback collection
  - Rate limiting

- **Phase 2 (Could Have):**
  - Omnichannel support (SMS, WhatsApp)
  - Authenticated user personalization
  - CRM integration
  - Multilingual support

## Documentation

- [Project Specification](docs/project-spec.md)
- [API Specification](docs/api-specification.yaml)
- [Database Schema](docs/database-schema.md)
- [User Stories](docs/user-stories.md)
- [Prioritization](docs/prioritization.md)
- [Risk Analysis](docs/risk-analysis.md)
- [Chat Interface Wireframe](docs/wireframes/chat-interface.md)

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Run tests: `uv run pytest` (backend) and `npm test` (frontend)
5. Submit a pull request

## License

MIT
