# SentinelAI System Architecture

## Architecture Status

Status: Proposed MVP Architecture

---

## Overview

SentinelAI uses a layered architecture to separate:

- external interfaces,
- application logic,
- AI orchestration,
- operational tools,
- persistence,
- enterprise identity,
- AI infrastructure.

---

## Logical Components

### API Layer

Provides external REST interfaces.

Technology:

- FastAPI

Responsibilities:

- request validation,
- authentication integration,
- API routing,
- response serialization.

---

### Application Services

Contains business use cases.

Responsibilities include:

- incident lifecycle management,
- investigation initiation,
- remediation workflow,
- approval workflow.

---

### Agent Orchestrator

Coordinates AI-assisted investigation.

Responsibilities:

- select investigation tools,
- collect context,
- request knowledge retrieval,
- produce structured investigation results,
- enforce execution limits.

---

### Evidence Engine

Normalizes operational evidence before presenting it to the model.

Evidence sources include:

- service telemetry,
- logs,
- deployment history,
- historical incidents,
- runbooks.

---

### Retrieval Layer

Provides retrieval-augmented generation capabilities.

Planned pipeline:

```text
Document
  |
  v
Parsing
  |
  v
Chunking
  |
  v
Embedding
  |
  v
PostgreSQL + pgvector
  |
  v
Similarity Retrieval
  |
  v
Reranking
  |
  v
Agent Context

```

## Tool Layer

Provides explicitly defined operations the agent may invoke.

Tools are categorized by risk.

### Read Tools

#### Examples:

- get_service_health,
- get_recent_logs,
- get_recent_deployments,
- search_runbooks,
- search_incidents.

### Write Tools

#### Examples::

- switch_payment_provider,
- restart_service,
- rollback_deployment.

Write tools require additional authorization and potentially human approval.

---

## Persistence

#### PostgreSQL will store:

- users,
- incidents,
- evidence,
- investigations,
- recommendations,
- approvals,
- tool executions,
- audit events.

pgvector will store embeddings for operational knowledge.

---

## WSO2 Integration

### AI Gateway

The AI Gateway sits between SentinelAI and model/MCP providers.

Its role is infrastructure governance rather than AI reasoning.

### Identity Platform

Identity Platform will provide authentication and authorization for users and
AI-agent interactions.

### MCP

Controlled operational capabilities may be exposed as MCP tools.

---