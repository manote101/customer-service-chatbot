# Risk Analysis

This risk analysis focuses on the MVP customer service chatbot (React frontend + FastAPI backend + PostgreSQL) including chat transcripts, escalation handoff, and knowledge-based answers.

Scales used:
- **Probability:** Low / Medium / High
- **Impact:** Low / Medium / High

## Technical Risks
1. **WebSocket connection stability**
   - Probability: Medium
   - Impact: High
   - Mitigation: Implement reconnection logic, fallback to polling

2. **API performance and latency under load**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Add timeouts, caching for common FAQs, and basic load testing; monitor p95 latency

3. **External integration failures (CRM/OMS/order lookup)**
   - Probability: Medium
   - Impact: High
   - Mitigation: Circuit breakers, retries with backoff, graceful degradation (provide ticket creation/handoff when tools are down)

4. **Inconsistent session handling / lost context**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Persist `session_id` and conversation state server-side; ensure idempotent session creation

5. **Knowledge base drift / stale answers**
   - Probability: High
   - Impact: High
   - Mitigation: Define content owners and update cadence; version control content; add “last updated” metadata and review workflow

6. **Data model mismatch between API and storage**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Validate request/response schemas; add integration tests; keep OpenAPI + models in sync

7. **Observability gaps (hard to debug issues)**
   - Probability: Medium
   - Impact: High
   - Mitigation: Structured logging, request IDs, basic metrics (error rate, latency), alerting on elevated failures

## Project Risks
1. **Scope creep from additional feature requests**
   - Probability: High
   - Impact: Medium
   - Mitigation: Strict backlog grooming, MVP focus

2. **Unclear success criteria / shifting KPIs**
   - Probability: Medium
   - Impact: High
   - Mitigation: Agree on KPIs upfront (containment, CSAT, response time); define pilot success thresholds

3. **Insufficient stakeholder alignment on escalation workflow**
   - Probability: Medium
   - Impact: High
   - Mitigation: Define required handoff fields, ticket routing, business hours rules; run agent walkthrough before launch

4. **Content readiness delays (FAQs/policies not available or not authoritative)**
   - Probability: Medium
   - Impact: High
   - Mitigation: Start with a small, curated set of high-traffic articles; establish ownership and SLA for updates

5. **Underestimating compliance/privacy requirements**
   - Probability: Medium
   - Impact: High
   - Mitigation: Document data retention; restrict access to transcripts; perform a lightweight privacy review before pilot

6. **Operational readiness gaps at launch**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Define on-call/triage process; add health checks; create runbook for common failures

## Security Risks
1. **Data leakage through chat logs**
   - Probability: Low
   - Impact: High
   - Mitigation: Encryption at rest and in transit, access controls

2. **PII over-collection (customers paste passwords, card numbers, addresses)**
   - Probability: High
   - Impact: High
   - Mitigation: Add input redaction patterns; warn users not to share sensitive data; restrict logging of raw content

3. **Prompt injection / instruction hijacking (if using LLM + retrieval)**
   - Probability: Medium
   - Impact: High
   - Mitigation: Use system constraints; restrict tools; only answer from trusted sources; ignore user attempts to override policies

4. **Unauthorized access to account/order data**
   - Probability: Medium
   - Impact: High
   - Mitigation: Strong authentication/verification for account-specific actions; least-privilege service credentials

5. **Insecure CORS configuration in production**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Lock down allowed origins; avoid `*` in production; validate cookies/credentials settings

6. **Rate limiting / abuse (spam, scraping, denial-of-service)**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Add per-IP/session limits; bot detection; backpressure and 429 responses

7. **Supply-chain risk in dependencies**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Pin versions (uv lockfile), vulnerability scanning, timely patching policy

## Operational & Product Risks
1. **Wrong answers reduce trust and increase contact rate**
   - Probability: Medium
   - Impact: High
   - Mitigation: Confidence thresholds; “I’m not sure” fallbacks; fast escalation; continuous review of failure cases

2. **Agent dissatisfaction if escalations are low-quality**
   - Probability: Medium
   - Impact: Medium
   - Mitigation: Include transcript + key fields; collect agent feedback; iterate on intake questions

3. **Transcript retention conflicts with privacy expectations**
   - Probability: Medium
   - Impact: High
   - Mitigation: Define retention window; implement deletion/archival; limit access via RBAC; document purpose

## Risk Owners (Suggested)
- **Engineering:** API reliability, integrations, observability, dependency management
- **Support Ops:** escalation workflow, content readiness, agent feedback loop
- **Security/Privacy:** PII handling, access controls, retention policy

## Review Cadence
- Review risks weekly during MVP build.
- Reassess before pilot and again before general availability.