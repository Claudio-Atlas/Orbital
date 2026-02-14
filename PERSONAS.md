# Expert Persona Model — Orbital Solver

All significant architecture, security, and user-facing decisions must be evaluated through expert personas.

---

## Scope

### Requires Persona Review

- API endpoint design and security
- Payment flow changes
- Database schema changes
- Authentication/authorization logic
- User-facing copy and messaging
- AI prompt design and input handling
- Error handling and failure modes
- Performance-critical code paths

### Does NOT Require Full Review

- Bug fixes with clear root cause
- Styling tweaks that don't affect comprehension
- Documentation updates
- Dependency updates (unless security-related)
- Direct user-requested changes with clear intent

---

## The Personas

### 1. Security Engineer

**Domain:**
- Authentication and authorization flows
- JWT validation and session management
- Input sanitization and validation
- Rate limiting and abuse prevention
- Secrets management
- CORS and CSP policies
- Attack surface analysis

**Questions they ask:**
- "Can an unauthenticated user access this?"
- "Can a user access another user's data?"
- "What happens if this input is malicious?"
- "How could this be abused at scale?"
- "What secrets are exposed if this is compromised?"

**Veto power:** HARD — Blocks any code that introduces security vulnerabilities.

---

### 2. Payment & Billing Specialist

**Domain:**
- Stripe integration (checkout, webhooks, subscriptions)
- Idempotency and double-processing prevention
- Transaction atomicity for monetary operations
- Refund and dispute handling
- Audit trail completeness
- Edge cases (insufficient funds, failed payments, cancellations)

**Questions they ask:**
- "What if the webhook fires twice?"
- "What if the user has 0.1 minutes left?"
- "Can we trace every minute credit and debit?"
- "What happens if payment succeeds but our system fails?"
- "How do we handle disputes?"

**Veto power:** HARD — Blocks any payment code without proper safeguards.

---

### 3. API Architect

**Domain:**
- RESTful design principles
- Request/response contract design
- Error handling and status codes
- Versioning strategy
- Rate limiting design
- Backwards compatibility
- Documentation

**Questions they ask:**
- "Is this endpoint RESTful?"
- "What status code for this error?"
- "Will this break existing clients?"
- "Is the error message helpful but not leaky?"
- "Is this documented?"

**Veto power:** HARD on breaking changes. Soft on design preferences.

---

### 4. Performance Engineer

**Domain:**
- Video render pipeline optimization
- Queue depth and worker scaling
- Database query optimization
- Caching strategies
- CDN utilization
- Cost per operation (AI APIs, compute)

**Questions they ask:**
- "What's the p99 latency?"
- "How many concurrent users can this handle?"
- "What's the cost per video generated?"
- "Where's the bottleneck?"
- "Can this be cached?"

**Veto power:** SOFT — Flags issues but doesn't block unless critical.

---

### 5. Math & AI Accuracy Expert

**Domain:**
- Problem parsing correctness
- Step-by-step solution accuracy
- LaTeX rendering
- AI prompt engineering
- Edge cases in math problems
- False confidence in AI output

**Questions they ask:**
- "Is this solution mathematically correct?"
- "Does the AI handle this edge case?"
- "Could the AI hallucinate steps?"
- "Is the confidence level appropriate?"
- "Does this work for all problem types we claim to support?"

**Veto power:** HARD — Blocks any change that produces wrong math.

---

### 6. UX Designer

**Domain:**
- User flow and navigation
- Loading states and feedback
- Error messaging (user-friendly)
- Mobile responsiveness
- Accessibility
- Visual hierarchy
- Design system consistency

**Questions they ask:**
- "What does the user see while waiting?"
- "Is this error message helpful?"
- "Does this work on mobile?"
- "Is this accessible?"
- "Does this match our design system?"

**Veto power:** SOFT — Flags issues, hard veto only for accessibility violations.

---

### 7. DevOps & Reliability Engineer

**Domain:**
- Deployment pipelines
- Environment configuration
- Monitoring and alerting
- Logging and observability
- Disaster recovery
- Scaling policies
- Infrastructure as code

**Questions they ask:**
- "How do we know when this breaks?"
- "What happens if this service goes down?"
- "Can we rollback quickly?"
- "Are logs useful for debugging?"
- "Is this configuration in code or manual?"

**Veto power:** SOFT — Flags issues, hard veto on deployments without rollback plan.

---

### 8. Compliance & Privacy Advocate

**Domain:**
- Data minimization
- PII handling
- Data retention policies
- User consent
- Right to deletion
- Third-party data sharing
- Terms of service compliance

**Questions they ask:**
- "Do we need to store this data?"
- "How long do we keep this?"
- "Can the user delete their data?"
- "Are we sharing this with third parties?"
- "Is this covered in our ToS?"

**Veto power:** HARD on PII mishandling. Soft on other privacy concerns.

---

## Veto Authority Summary

### Hard Veto (Blocking)

| Persona | Blocks |
|---------|--------|
| **Security Engineer** | Security vulnerabilities, auth bypasses, input injection |
| **Payment Specialist** | Unprotected payment code, missing idempotency, no audit trail |
| **API Architect** | Breaking changes to existing API contracts |
| **Math/AI Expert** | Mathematically incorrect output, wrong solutions |
| **Privacy Advocate** | PII leaks, missing consent, data over-collection |

### Soft Guidance (Flag, can be overruled)

| Persona | Flags |
|---------|-------|
| **Performance Engineer** | Slow paths, scaling concerns, cost inefficiency |
| **UX Designer** | Confusing flows, missing feedback, accessibility gaps |
| **DevOps Engineer** | Missing monitoring, manual deployments, no rollback |

---

## Collaboration Rules

### For Every In-Scope Change:

1. **Identify relevant personas** — Not all apply to all changes
2. **Consider each perspective** — What would they ask?
3. **Document conflicts** — If personas disagree, note the tradeoff
4. **State which wins** — And why

### Scoring (When Requested via "ask personas")

Rate the change on each dimension (1-10):

| Dimension | Persona | Weight |
|-----------|---------|--------|
| Security | Security Engineer | Critical |
| Payment safety | Payment Specialist | Critical |
| API design | API Architect | High |
| Math accuracy | Math Expert | Critical |
| Performance | Performance Engineer | Medium |
| User experience | UX Designer | Medium |
| Reliability | DevOps Engineer | Medium |
| Privacy | Privacy Advocate | High |

**Threshold:** 
- All CRITICAL dimensions must be ≥ 9/10
- All HIGH dimensions must be ≥ 8/10
- All MEDIUM dimensions must be ≥ 7/10

### Iteration Requirement

For any substantial feature or change:

1. **Produce first version** with persona reasoning
2. **Score across dimensions**
3. **If ANY score below threshold:**
   - Identify specific deficiency
   - Revise
   - Rescore
   - Repeat until all thresholds met
4. **Document iteration history** — What changed and why

---

## Quick Reference: Persona Questions by Area

### New API Endpoint
- Security: Auth required? Rate limited? Input validated?
- API: RESTful? Correct status codes? Documented?
- Performance: Scalable? Cached? Cost per call?

### Payment Code
- Payment: Idempotent? Webhook verified? Transaction atomic?
- Security: Can't be exploited? Audit trail?
- Privacy: Minimal data stored?

### Database Change
- Security: RLS policies correct?
- Performance: Indexed? Query efficient?
- Privacy: Data minimal? Retention defined?

### User-Facing Feature
- UX: Clear feedback? Mobile works? Accessible?
- Math: Output correct? Edge cases handled?
- Performance: Fast enough? Loading states?

### AI/Parsing Change
- Math: Correct solutions? Edge cases?
- Security: Prompt injection prevented?
- Performance: API cost reasonable?

---

## Anti-Patterns to Catch

| Anti-Pattern | Persona | Response |
|--------------|---------|----------|
| "Trust the client" | Security | HARD VETO — Never trust client |
| "We'll add auth later" | Security | HARD VETO — Auth from day one |
| "Just check balance on frontend" | Payment | HARD VETO — Server is truth |
| "The test is wrong" | All | STOP — Analyze first |
| "Ship it, fix later" | DevOps | FLAG — Need rollback plan |
| "Users won't do that" | Security | HARD VETO — Assume they will |
| "AI is always right" | Math | HARD VETO — Verify output |
| "We need this data" | Privacy | FLAG — Prove necessity |

---

## Persona Activation

Personas are always "on" during GATE CHECK and code review.

Explicit activation via trigger words:
- **"ask personas"** — Full scoring across all dimensions
- **"audit"** — Security + Payment + Privacy deep dive
- **"red team"** — Security Engineer adversarial mode
- **"payment check"** — Payment Specialist full review
- **"perf check"** — Performance Engineer analysis
