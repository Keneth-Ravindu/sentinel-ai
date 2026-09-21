# Investigation Engine

## Purpose

The Investigation Engine collects and normalizes operational
evidence associated with a SentinelAI incident.

It is intentionally deterministic and does not currently use
a language model.

This ensures that operational evidence can be collected and
validated independently of AI reasoning.

## Investigation Flow

```text
Incident
   |
   v
Investigation Service
   |
   +--> Service Health Tool
   |
   +--> Recent Logs Tool
   |
   +--> Deployment History Tool
   |
   v
Evidence Collection
   |
   v
Deterministic Signal Extraction
   |
   v
Investigation Snapshot
```

## Read-Only Tools

### get_service_health

Retrieves:

- service status,
- CPU utilization,
- memory utilization,
- error rate,
- P95 latency,
- database latency,
- active payment provider.

### get_recent_logs

Retrieves operational log events associated with the
investigated service.

### get_recent_deployments

Retrieves deployment history associated with the investigated
service.

## Signal Extraction

The Investigation Engine derives deterministic signals from
operational evidence.

Current signals include:

- high error rate,
- high P95 latency,
- normal CPU utilization,
- normal memory utilization,
- normal database latency,
- payment-provider timeout detection,
- circuit-breaker warning detection,
- recent deployment detection.

Signals represent observed conditions.

They do not represent a final root-cause conclusion.

## AI Boundary

The Investigation Engine does not ask an LLM to determine
operational facts.

Instead:

```text
Operational Systems
        |
        v
Deterministic Tools
        |
        v
Structured Evidence
        |
        v
Deterministic Signals
        |
        v
AI Reasoning Layer
``` 
