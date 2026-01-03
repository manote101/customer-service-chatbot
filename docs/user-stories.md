# User Stories

## Customer Stories
1. As a customer, I want to ask questions in natural language so that I can get help quickly without reading documentation.
2. As a customer, I want to see suggested topics (e.g., order status, returns, shipping) so that I can quickly choose what I need.
3. As a customer, I want the chatbot to ask clarifying questions when my request is ambiguous so that I can get an accurate answer.
4. As a customer, I want help tracking an order so that I can understand where my package is.
5. As a customer, I want to learn the return and refund policy so that I know whether I’m eligible.
6. As a customer, I want to start a return flow (where supported) so that I can resolve issues without waiting for an agent.
7. As a customer, I want to get answers about shipping options and delivery timeframes so that I can plan accordingly.
8. As a customer, I want to get product help (compatibility, sizing, warranty basics) so that I can use the product successfully.
9. As a customer, I want to request a human agent when the chatbot can’t help so that I can still resolve my issue.
10. As a customer, I want the chatbot to remember the context of my conversation so that I don’t need to repeat myself.
11. As a customer, I want to provide feedback at the end of the chat so that the team can improve support quality.

### Customer Acceptance Criteria (MVP)
- Chat UI accepts free-text messages and returns a response.
- Chatbot asks for missing required details (e.g., order number) rather than guessing.
- Chatbot can handle follow-up questions in the same session.
- Customer can initiate escalation to a human agent at any point.
- End-of-chat feedback (CSAT) can be submitted.

## Agent Stories
1. As a customer service agent, I want to see conversation history so that I understand the context when a chat is escalated.
2. As a customer service agent, I want the escalation to include structured fields (e.g., reason, order number, contact email) so that I can help faster.
3. As a customer service agent, I want to know what the chatbot already asked/answered so that I don’t repeat steps.
4. As a customer service agent, I want escalations routed with an issue category so that tickets go to the right queue.
5. As a customer service agent, I want to see whether the user is authenticated so that I can follow the correct verification process.

### Agent Acceptance Criteria (MVP)
- Escalations include a transcript plus a short summary of the customer request.
- Escalations include any collected identifiers (e.g., order number) if provided.
- Escalations include a reference ID (ticket ID or conversation/session ID).

## Admin Stories
1. As a system administrator, I want to monitor chatbot performance so that I can identify issues before customers are affected.
2. As a system administrator, I want to view key metrics (usage, containment/deflection, error rate) so that I can track effectiveness over time.
3. As a system administrator, I want to review failed or escalated conversations so that I can identify gaps in coverage.
4. As a system administrator, I want to update knowledge content (policies/FAQs) so that the chatbot answers reflect the latest information.
5. As a system administrator, I want to configure escalation rules (e.g., business hours, low-confidence handoff) so that customers get timely help.
6. As a system administrator, I want to enforce data retention rules for transcripts so that we meet privacy and compliance expectations.

### Admin Acceptance Criteria (MVP)
- Service health can be checked via an endpoint (e.g., `/health`).
- Basic operational visibility exists (logs/metrics sufficient to debug failures).
- Knowledge base content has a defined ownership and update process (initially via docs in repo).
- Transcript retention policy is documented (and implementable in scheduled jobs).
