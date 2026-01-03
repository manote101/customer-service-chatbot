from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4
import logging

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app import models
from app.knowledge import find_best_faq, detect_intent

# Create tables (for MVP; in production use Alembic migrations)
models.Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Customer Service Chatbot API",
    description="Backend API for customer service chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatUser(BaseModel):
    id: Optional[str] = None
    is_authenticated: bool = False


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    user: Optional[ChatUser] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[datetime] = None


class Handoff(BaseModel):
    recommended: bool
    reason: Optional[str] = None
    ticket_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: Optional[str] = None
    reply: str
    messages: Optional[List[ChatMessage]] = None
    handoff: Optional[Handoff] = None


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str

@app.get("/")
async def root():
    return {"message": "Welcome to Customer Service Chatbot API"}


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="customer-service-chatbot")


def _generate_reply(message: str, intent: str, confidence: Optional[float]) -> tuple[str, Optional[Handoff]]:
    """Generate bot reply based on intent and knowledge base."""
    
    # Check for agent escalation intent
    if intent == "escalation":
        return (
            "I'll connect you with a support agent. Please provide your email and a brief description of your issue.",
            Handoff(recommended=True, reason="User requested human assistance"),
        )
    
    # Try FAQ matching first
    faq_match = find_best_faq(message)
    if faq_match:
        faq, faq_confidence = faq_match
        logger.info(f"FAQ match: {faq.question} (confidence: {faq_confidence:.1f}%)")
        return faq.answer, None
    
    # Intent-specific fallbacks
    if intent == "order_tracking":
        return "I can help you track your order. Please provide your order number (format: ORD-12345).", None
    elif intent == "returns":
        return "I can help with returns. Could you provide your order number so I can look up the details?", None
    
    # Generic fallback
    return (
        "I'd be happy to help! Could you provide a bit more detail? I can assist with:\n"
        "• Order tracking\n"
        "• Returns & refunds\n"
        "• Shipping info\n"
        "• Account questions\n\n"
        "Or type 'agent' to speak with a person.",
        None,
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """Process a chat message and return bot response."""
    try:
        # Get or create conversation
        conversation = None
        if request.session_id:
            conversation = db.query(models.Conversation).filter_by(
                session_id=request.session_id
            ).first()
        
        if not conversation:
            session_id = request.session_id or f"sess_{uuid4().hex}"
            conversation = models.Conversation(
                session_id=session_id,
                channel="web",
                locale=request.metadata.get("locale") if request.metadata else None,
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            logger.info(f"Created new conversation: {conversation.session_id}")
        
        # Detect intent
        intent, extracted_value = detect_intent(request.message)
        logger.info(f"Intent: {intent}, Extracted: {extracted_value}")
        
        # Save user message
        user_message = models.Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message,
            intent=intent,
            extra_data={"extracted_value": extracted_value} if extracted_value else None,
        )
        db.add(user_message)
        
        # Generate reply
        reply_text, handoff_data = _generate_reply(request.message, intent, None)
        
        # Save assistant message
        assistant_message = models.Message(
            conversation_id=conversation.id,
            role="assistant",
            content=reply_text,
        )
        db.add(assistant_message)
        
        # Create handoff if recommended
        if handoff_data:
            handoff_record = models.Handoff(
                conversation_id=conversation.id,
                recommended=handoff_data.recommended,
                reason=handoff_data.reason,
                status="pending",
            )
            db.add(handoff_record)
        
        db.commit()
        
        # Build response with recent messages
        recent_messages = db.query(models.Message).filter_by(
            conversation_id=conversation.id
        ).order_by(models.Message.created_at.desc()).limit(10).all()
        
        message_list = [
            ChatMessage(
                role=msg.role,
                content=msg.content,
                timestamp=msg.created_at,
            )
            for msg in reversed(recent_messages)
        ]
        
        return ChatResponse(
            session_id=conversation.session_id,
            reply=reply_text,
            messages=message_list,
            handoff=handoff_data,
        )
    
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

