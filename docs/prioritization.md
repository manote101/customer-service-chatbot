# Feature Prioritization

## MUST HAVE (MVP)
1. Basic chat interface
2. Message sending/receiving
3. Simple intent recognition
4. FAQ/policy answers from a curated knowledge source (at minimum: a small, maintained set of Q&A)
5. Clarifying questions for missing details (e.g., order number)
6. Human handoff path ("Talk to an agent") with transcript and collected fields
7. Conversation session tracking (session_id) to preserve context across messages
8. Basic safety/privacy handling (minimize PII collection; avoid logging secrets)
9. Health endpoint and basic operational logging (so we can monitor uptime and failures)

## SHOULD HAVE (Phase 1)
1. File attachments
2. Conversation history
3. Basic analytics
4. Customer feedback capture (CSAT/thumbs up/down) at end of chat
5. Admin/content update workflow for knowledge base (even if initially via docs + redeploy)
6. Rate limiting and abuse/spam controls
7. Improved intent routing for top intents (order status, returns, shipping, billing)
8. Better escalation routing (category/queue) and required-field validation for handoff

## COULD HAVE (Phase 2)
1. Voice input
2. Advanced NLP
3. CRM integration
4. Omnichannel support (SMS/WhatsApp/Messenger)
5. Personalization for authenticated users (order lookups, account-specific help)
6. Proactive notifications (order shipped, refund processed)
7. A/B testing for prompts/flows and automated conversation review
8. Multilingual support beyond a single primary locale

## WON'T HAVE (Phase 3+ or Never)
1. Video chat
2. Augmented reality support
3. Blockchain integration
4. Fully autonomous refunds/chargebacks without explicit business approval and strong verification
5. Replacing all human support (the bot will always have a human escalation path)
6. Legal/medical/financial advice capabilities