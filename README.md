# SentinelAI

> Enterprise agentic AI for intelligent production incident investigation and response.

SentinelAI is an AI-powered incident intelligence and response platform designed
to help engineering and operations teams investigate production incidents faster,
correlate evidence across operational systems, identify likely root causes,
recommend remediation, and safely execute human-approved actions.

---

## Problem

Modern engineering teams operate increasingly distributed systems consisting of:

- APIs
- microservices
- databases
- cloud infrastructure
- third-party services
- deployment pipelines
- observability platforms
- operational documentation

When a production incident occurs, engineers often need to manually search across
multiple systems to determine:

- what failed,
- when the failure began,
- what changed,
- which systems are affected,
- whether the issue has occurred before,
- which runbook applies,
- and which remediation action should be taken.

This investigation process can increase Mean Time To Resolution (MTTR) and place
significant cognitive load on incident responders.

---

## Solution

SentinelAI acts as an AI-powered investigation layer across operational systems.

When an incident occurs, SentinelAI can:

1. collect service health information,
2. inspect relevant logs,
3. review deployment history,
4. search historical incidents,
5. retrieve operational runbooks,
6. correlate evidence,
7. produce an evidence-backed root-cause hypothesis,
8. recommend remediation,
9. request human approval for sensitive actions,
10. execute approved operational tools,
11. verify service recovery,
12. generate a post-incident summary.

---

## Core Principle

SentinelAI follows a human-in-the-loop approach:

> AI investigates.  
> Evidence grounds it.  
> WSO2 governs it.  
> Humans authorize it.

The AI may recommend operational changes, but sensitive production actions must
pass deterministic authorization and approval controls.

---

## Example Scenario

A payment microservice experiences:

- elevated HTTP 5xx errors,
- increased response latency,
- repeated external provider timeouts,
- normal CPU usage,
- normal database latency.

SentinelAI investigates service metrics, logs, deployments, historical incidents,
and operational runbooks.

It identifies external payment-provider degradation as the likely root cause and
recommends routing traffic to a configured backup provider.

An authorized incident commander reviews and approves the action before the
remediation tool is executed.

SentinelAI then monitors recovery and verifies that the error rate has returned
to normal levels.

---

## Planned MVP

The first MVP will provide:

- incident creation and tracking,
- simulated microservice infrastructure,
- operational telemetry tools,
- log investigation,
- deployment-history investigation,
- runbook retrieval,
- historical incident retrieval,
- RAG-based operational knowledge search,
- AI-assisted root-cause analysis,
- structured evidence reporting,
- remediation recommendations,
- human approval workflows,
- simulated remediation,
- incident recovery verification,
- audit logging,
- AI evaluation.

---

## WSO2 Integration

SentinelAI is being designed around enterprise AI governance.

Planned WSO2 integrations include:

### WSO2 AI Gateway

Used to govern AI traffic between SentinelAI and supported LLM providers.

Planned responsibilities include:

- secured LLM connectivity,
- provider abstraction,
- traffic policies,
- guardrails,
- observability,
- rate limiting,
- governed MCP traffic.

### WSO2 Identity Platform

Used for:

- user authentication,
- role-based authorization,
- agent identities,
- delegated authorization,
- OAuth/OIDC,
- approval permissions.

### MCP

Operational capabilities will be exposed as controlled tools that an AI agent
can discover and invoke.

Sensitive tools will require authorization and, where applicable, explicit human
approval.

---

## Proposed Architecture

```text
                         Engineering User
                                |
                                v
                       SentinelAI Web UI
                                |
                                v
                    WSO2 Identity Platform
                                |
                             OAuth/OIDC
                                |
                                v
                       SentinelAI Backend
                          FastAPI / Python
                                |
                                v
                       Agent Orchestrator
                     /          |           \
                    /           |            \
                   v            v             v
               RAG Engine   Evidence Engine   Tool Router
                   |                            |
                   v                            v
           PostgreSQL + pgvector         MCP / APIs
                                                |
                                                v
                                        WSO2 AI Gateway
                                       /               \
                                      v                 v
                                  LLM APIs         MCP Servers
```
---
## Technology Stack
- Backend
    - Python 3.11
    - FastAPI
    - Pydantic
    - SQLAlchemy
    - PostgreSQL
- AI Engineering
    - Agentic workflows
    - Retrieval-Augmented Generation
    - embeddings
    - vector search
    - reranking
    - structured output
    - tool calling
    - MCP
    - evaluation
- AI Infrastructure
    - WSO2 AI Gateway
    - WSO2 Identity Platform
- Data
    - PostgreSQL
    - pgvector
- Frontend
    - React
    - Vite
    - plain CSS
- Infrastructure
    - Docker
    - Docker Compose
    - GitHub Actions
- Development
    - uv
    - pytest
    - Ruff
---

---

## AI Safety and Operational Controls

SentinelAI is designed so that language-model output is never treated as an
authorization decision.

Operational controls will include:

- deterministic permission checks,
- human approval for sensitive actions,
- structured tool schemas,
- restricted tool access,
- audit logging,
- prompt-injection protection,
- bounded agent execution,
- token/request limits,
- evidence attribution,
- post-action verification.

---

---

# License

Copyright (c) 2026 Keneth Ravindu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

