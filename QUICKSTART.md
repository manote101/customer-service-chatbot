# Quick Start Guide

## ✅ Your MVP is Ready!

### Currently Running:
- **Backend API:** http://localhost:8000
- **Frontend UI:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432

### What's Working:
✅ Chat interface with message bubbles
✅ Natural language FAQ responses
✅ Intent detection (orders, returns, escalation)
✅ Session persistence across messages
✅ Database storage (PostgreSQL)
✅ Agent escalation with handoff tracking
✅ Privacy warnings for PII
✅ Health monitoring

### Quick Commands:

**Stop All Services:**
```bash
# Stop frontend: Ctrl+C in the npm terminal
# Stop backend: pkill -f uvicorn
# Stop PostgreSQL: docker-compose down
```

**Restart Services:**
```bash
# Backend
cd backend
uv run uvicorn app.main:app --reload

# Frontend
cd frontend
npm start
```

**Run Tests:**
```bash
cd backend
uv run pytest -v
```

**Database:**
```bash
# View migrations
cd backend
uv run alembic history

# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head
```

### Test the Chatbot:

Try these messages:
- "How long does shipping take?"
- "What is your return policy?"
- "Where is my order?"
- "I need to speak with an agent"

### Next Steps:

1. **Customize FAQs:** Edit `backend/app/knowledge.py`
2. **Modify UI:** Update components in `frontend/src/components/`
3. **Add Features:** See `docs/prioritization.md` for roadmap
4. **Deploy:** Use `docker-compose up -d` for production

### Troubleshooting:

**Port already in use:**
```bash
# Kill processes on port 8000
sudo lsof -ti:8000 | xargs kill -9

# Kill processes on port 3000
sudo lsof -ti:3000 | xargs kill -9
```

**Database connection issues:**
```bash
docker-compose restart postgres
```

**Need clean install:**
```bash
# Backend
cd backend
rm -rf .venv
uv sync --extra dev

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```
