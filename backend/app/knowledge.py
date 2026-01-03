"""Simple in-memory FAQ/knowledge base for MVP.

In production, replace this with a proper retrieval system
(vector DB, full-text search, or external knowledge API).
"""

from typing import Optional, List, Tuple
import re


class FAQ:
    def __init__(self, question: str, answer: str, keywords: List[str]):
        self.question = question
        self.answer = answer
        self.keywords = [k.lower() for k in keywords]


# MVP Knowledge Base
FAQS = [
    FAQ(
        question="How do I track my order?",
        answer="I can help you track your order! Please provide your order number (it looks like ORD-12345).",
        keywords=["track", "order", "shipping", "package", "delivery", "where is"],
    ),
    FAQ(
        question="What is your return policy?",
        answer="We accept returns within 30 days of delivery. Items must be unused and in original packaging. To start a return, I'll need your order number.",
        keywords=["return", "refund", "exchange", "send back"],
    ),
    FAQ(
        question="How long does shipping take?",
        answer="Standard shipping takes 5-7 business days. Expedited shipping (2-3 days) is available at checkout. International orders typically take 10-14 business days.",
        keywords=["shipping", "delivery", "how long", "arrive", "when will"],
    ),
    FAQ(
        question="How do I reset my password?",
        answer="To reset your password, visit the login page and click 'Forgot Password'. You'll receive a reset link via email. If you don't see it, check your spam folder.",
        keywords=["password", "reset", "forgot", "login", "sign in", "account"],
    ),
    FAQ(
        question="Do you ship internationally?",
        answer="Yes! We ship to most countries. Shipping costs and delivery times vary by location. You'll see the exact cost at checkout.",
        keywords=["international", "ship", "country", "overseas", "abroad"],
    ),
    FAQ(
        question="What payment methods do you accept?",
        answer="We accept major credit cards (Visa, MasterCard, Amex), PayPal, and Apple Pay. All transactions are secure and encrypted.",
        keywords=["payment", "pay", "credit card", "paypal", "accept"],
    ),
]


def find_best_faq(message: str) -> Optional[Tuple[FAQ, float]]:
    """
    Simple keyword matching to find relevant FAQ.
    Returns (FAQ, confidence_score) or None.
    """
    message_lower = message.lower()
    
    best_match = None
    best_score = 0.0
    
    for faq in FAQS:
        score = 0
        matched_keywords = 0
        
        for keyword in faq.keywords:
            if keyword in message_lower:
                matched_keywords += 1
                # Longer keywords get higher weight
                score += len(keyword.split())
        
        if matched_keywords > 0:
            # Normalize by number of keywords in FAQ
            normalized_score = score / len(faq.keywords)
            if normalized_score > best_score:
                best_score = normalized_score
                best_match = faq
    
    # Only return if we have reasonable confidence
    if best_match and best_score > 0.15:
        # Convert to 0-100 scale, cap at 95 for simple keyword matching
        confidence = min(best_score * 100, 95)
        return best_match, confidence
    
    return None


def detect_intent(message: str) -> Tuple[str, Optional[str]]:
    """
    Detect user intent and extract any relevant entities.
    Returns (intent, extracted_value).
    """
    message_lower = message.lower()
    
    # Order tracking intent
    order_pattern = r'\b(ORD-\d+|#\d{5,}|\d{10,})\b'
    order_match = re.search(order_pattern, message, re.IGNORECASE)
    if order_match or any(kw in message_lower for kw in ["track", "where is my order", "order status"]):
        return "order_tracking", order_match.group(0) if order_match else None
    
    # Returns intent
    if any(kw in message_lower for kw in ["return", "refund", "send back", "exchange"]):
        return "returns", None
    
    # Agent escalation
    if any(kw in message_lower for kw in ["agent", "human", "representative", "person", "speak to"]):
        return "escalation", None
    
    # Default: FAQ search
    return "faq", None
