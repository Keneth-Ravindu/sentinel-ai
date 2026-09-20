# Incident Management API

## Purpose

The Incident Management API provides the lifecycle foundation for
SentinelAI incident investigation.

Base path:

`/api/v1/incidents`

---

## Incident Lifecycle

```text
OPEN
 |
 v
INVESTIGATING
 |          \
 v           \
MITIGATING    ---> RESOLVED
 |
 v
RESOLVED
```

---

## Create Incident

### Request

`POST /api/v1/incidents`
```json
{
  "service": "payment-service",
  "severity": "SEV-1",
  "description": "Payment authorization failures detected during peak traffic.",
  "error_rate": 19.8,
  "p95_latency_ms": 5200
}
```

### Response

```http
HTTP 201 Created
```
The system creates:

- a UUID,
- an OPEN status,
- created timestamp,
- updated timestamp.

--- 

### List Incidents

`GET /api/v1/incidents`

Returns incidents ordered from newest to oldest.

--- 

## Get Incident

`GET /api/v1/incidents/{incident_id}`

Returns HTTP 404 when the incident does not exist.

---

### Update Status

`PATCH /api/v1/incidents/{incident_id}/status`

Example:

```json
{
  "status": "INVESTIGATING"
}
```

Valid lifecycle transitions are enforced by the application
service.

Invalid transitions return:

```http
HTTP 409 Conflict
```

---

### Validation

Requests are validated using Pydantic.

Examples of rejected input include:

- error rates below 0,
- error rates above 100,
- negative latency,
- unsupported severity values,
- unsupported status values,
- empty service names,
- insufficient descriptions.

Validation failures return HTTP 422.
