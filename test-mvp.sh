#!/bin/bash
# Test the MVP functionality

echo "🧪 Testing Customer Service Chatbot MVP"
echo ""

# Test 1: Health check
echo "1️⃣ Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q "ok"; then
    echo "   ✅ Health check passed"
else
    echo "   ❌ Health check failed"
    exit 1
fi

# Test 2: Send a chat message
echo ""
echo "2️⃣ Testing chat endpoint..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How long does shipping take?"}')

if echo "$CHAT_RESPONSE" | grep -q "session_id"; then
    echo "   ✅ Chat endpoint passed"
    SESSION_ID=$(echo "$CHAT_RESPONSE" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $SESSION_ID"
else
    echo "   ❌ Chat endpoint failed"
    exit 1
fi

# Test 3: Session persistence
echo ""
echo "3️⃣ Testing session persistence..."
CHAT_RESPONSE2=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Thanks\", \"session_id\": \"$SESSION_ID\"}")

if echo "$CHAT_RESPONSE2" | grep -q "$SESSION_ID"; then
    echo "   ✅ Session persistence passed"
else
    echo "   ❌ Session persistence failed"
    exit 1
fi

# Test 4: FAQ matching
echo ""
echo "4️⃣ Testing FAQ knowledge base..."
FAQ_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your return policy?"}')

if echo "$FAQ_RESPONSE" | grep -qi "return"; then
    echo "   ✅ FAQ matching passed"
else
    echo "   ❌ FAQ matching failed"
fi

# Test 5: Agent escalation
echo ""
echo "5️⃣ Testing agent escalation..."
ESCALATION_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need to speak with an agent"}')

if echo "$ESCALATION_RESPONSE" | grep -q '"recommended":true'; then
    echo "   ✅ Agent escalation passed"
else
    echo "   ❌ Agent escalation failed"
fi

echo ""
echo "✅ All MVP tests passed!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
