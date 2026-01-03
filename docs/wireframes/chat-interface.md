# Chat Interface Wireframe

## Layout:
- Header: Company logo, chat title, minimize/close buttons
- Main Area: 
  - Message history (scrollable)
  - Each message bubble shows avatar, timestamp
- Footer:
  - Message input box
  - Attachment button
  - Send button
  - Quick reply chips (optional, shown when relevant)
  - Escalate button/link: “Talk to a person”
  - Character limit helper / remaining characters (optional)
  - Privacy hint (small text): “Do not share passwords or payment info.”

### Header Details
- Left: Logo (or brand mark) + title “Support Chat”
- Right: Minimize, Close
- Optional: Connection status indicator (e.g., “Online” / “Reconnecting…”) shown only when needed

### Message List Details
- Scroll container with newest messages at bottom
- Day separators (optional): “Today”
- Message bubble variants:
  - **Customer message (right aligned):** plain text
  - **Bot message (left aligned):** plain text + optional suggested actions (chips)
  - **System message (centered):** e.g., “Chat connected”, “Agent joined”, “Ticket created: #123”
- Each message shows:
  - timestamp (small)
  - optional avatar for bot/agent
  - error state on message (e.g., red “Not delivered” + retry)

### Footer Details
- Input field supports multi-line (Shift+Enter new line)
- Send button disabled when input empty
- Attachment button visible only if attachments are enabled for the phase
- Secondary actions row (below input):
  - Quick replies (chips)
  - “Talk to a person” link

## States:
1. Empty state: Welcome message
2. Active chat: Messages displayed
3. Typing indicator: "Bot is typing..."
4. Error state: "Failed to send"

### 1) Empty State (First Open)
- Bot greeting message:
  - “Hi! I’m the support assistant. What can I help you with?”
- Suggested topics (chips):
  - “Track an order”
  - “Returns & refunds”
  - “Shipping info”
  - “Product help”
- Footer enabled for free-text input

### 2) Active Chat State
- Message history visible and scrollable
- New messages append to bottom
- Auto-scroll to bottom if the user is already near bottom
- If the user has scrolled up, show a “Jump to latest” affordance

### 3) Bot Typing State
- Display typing indicator below the last bot message or at the bottom:
  - “Support bot is typing…”
- Disable send? (No) — user can continue typing while bot responds

### 4) Error State
- Triggered on network/API failure
- UI behavior:
  - Show inline error on the failed message: “Not delivered”
  - Provide “Retry” action
  - If the whole chat is offline, show banner: “Reconnecting…”

## Key Interactions

### Send Message
1. Customer types message
2. Customer clicks Send (or presses Enter)
3. UI shows the customer message immediately (optimistic)
4. Client calls `POST /api/v1/chat`
5. On success, bot reply appears and typing indicator disappears
6. On failure, message shows error + Retry

### Session Handling
- Client stores `session_id` after first response
- Subsequent sends include `session_id` to preserve context

### Quick Replies / Chips
- When bot provides suggested actions, chips appear beneath the bot message
- Clicking a chip sends a pre-filled message (or triggers a defined flow)

### Escalation (Talk to a Person)
- “Talk to a person” is always available
- When selected:
  - Bot asks for required handoff fields (e.g., email, order number) if missing
  - UI shows a system message when escalation is created (e.g., “Ticket created: #…”) or agent joins

## Accessibility Notes (MVP)
- All interactive controls are keyboard accessible
- Input has an accessible label (e.g., “Message”) and Send has a clear name
- New messages announce politely via aria-live region (avoid interrupting typing)

## Copy/Content Guidelines
- Friendly, concise bot language
- Avoid claims of certainty when unsure; ask clarifying questions
- Prominent privacy note: “Do not share passwords or full payment card numbers.”
