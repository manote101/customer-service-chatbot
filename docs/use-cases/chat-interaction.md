# Use Case: Chat Interaction

## Primary Actor: Customer

## Preconditions:
1. Customer visits support website
2. Chat widget is available and active

## Main Flow:

1. Customer opens the chat widget.
2. Chatbot greets the customer and prompts for how it can help (e.g., order status, returns, shipping, billing).
3. Customer submits a question or request in natural language.
4. Chatbot classifies the customer’s intent and extracts relevant details (e.g., order number, email, product name).
5. If required details are missing, the chatbot asks a clarifying question.
6. Customer provides the requested details.
7. Chatbot retrieves the most relevant support content and/or calls backend services (e.g., order lookup) to generate an answer.
8. Chatbot responds with the resolution steps or requested information.
9. Customer indicates the issue is resolved or asks a follow-up question.
10. If the customer asks a follow-up, the chatbot maintains context and repeats steps 4–9.
11. If the chatbot cannot confidently resolve the issue, it offers escalation to a human agent.
12. If customer accepts escalation, the chatbot collects any required handoff fields (e.g., contact email, order number, issue summary).
13. Chatbot creates a support ticket or routes to a live agent and transfers the conversation transcript and collected metadata.
14. Chatbot confirms the escalation outcome (ticket created / agent connected) and provides any reference ID.
15. Chatbot requests feedback (e.g., CSAT) and ends the conversation.
