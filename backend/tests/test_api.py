import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import Base, engine
from app import models


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_returns_welcome_message() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Customer Service Chatbot API"}


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "customer-service-chatbot"}


def test_chat_requires_message() -> None:
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422


def test_chat_returns_reply_and_session_id() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Where is my order?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["reply"]
    assert body["session_id"].startswith("sess_")
    assert len(body["messages"]) >= 2
    assert body["messages"][0]["role"] == "user"
    assert body["messages"][1]["role"] == "assistant"


def test_chat_preserves_session() -> None:
    """Test that conversation context is preserved across messages."""
    # First message
    response1 = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
    )
    assert response1.status_code == 200
    session_id = response1.json()["session_id"]
    
    # Second message with same session
    response2 = client.post(
        "/api/v1/chat",
        json={
            "message": "Track my order",
            "session_id": session_id,
        },
    )
    assert response2.status_code == 200
    assert response2.json()["session_id"] == session_id
    # Should have more messages now
    assert len(response2.json()["messages"]) >= 4


def test_chat_detects_escalation_intent() -> None:
    """Test that agent request triggers handoff."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "I need to speak with an agent"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["handoff"] is not None
    assert body["handoff"]["recommended"] is True


def test_chat_matches_faq() -> None:
    """Test that FAQ keywords are matched."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "How long does shipping take?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "shipping" in body["reply"].lower() or "delivery" in body["reply"].lower()
