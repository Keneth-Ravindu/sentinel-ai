# SentinelAI Security Model

## Objective

The SentinelAI security model ensures that AI-assisted investigation does not
translate into unrestricted access to operational systems.

---

## Core Security Principle

A language model is not an authorization system.

All security decisions must be enforced using deterministic application and
identity policies.

---

## Identity Types
SentinelAI distinguishes between:

- human users,
- applications,
- AI agents,
- operational tools.

Each identity should receive only the permissions required for its function.

---

## Authentication

Planned authentication uses OAuth 2.0 and OpenID Connect through WSO2 Identity
Platform.

---

## Authorization

Authorization will use explicit permissions and roles.

Example permissions:

```text
incident:read
incident:create
incident:investigate

remediation:request
remediation:approve
remediation:execute

audit:read
```

Example roles:

```text
Viewer
Engineer
IncidentCommander
Administrator
```

---

## Tool Authorization

Each tool is assigned a risk classification.

### Low Risk

Read-only operations.

Example: 

```text
get_service_health
get_logs
search_runbooks
```

### High Risk

Operations that modify system state.

Example:

```text
switch_payment_provider
restart_service
rollback_deployment
```

High-risk tools require:

1. valid authentication,
2. required permission,
3. valid incident context,
4. explicit human approval,
5. audit logging.

---

## Prompt Injection

Operational content such as logs and documents is treated as untrusted data.

Instructions contained within retrieved logs or documents must never override
system policies or tool authorization.

---

## Secrets
Secrets must:

- never be committed to Git,
- never appear in .env.example,
- never be returned to the LLM unless explicitly required and safely scoped,
- be stored using secure secret-management mechanisms in production.    

---

## Audit Requirements

The following events should be recorded:

- authentication
- incident creation
- investigation start
- retrieval execution
- model invocation
- tool invocation
- approval request
- approval or rejection
- remediation execution
- incident resolution

---

## Human-in-the-Loop

Sensitive operational changes require explicit human approval.

Approval must occur outside the LLM reasoning process.

The model may recommend an action but cannot grant its own permission to execute
that action.