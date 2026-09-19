# SentinelAI MVP Scope

## MVP Scenario

The initial MVP focuses on one production incident:

**External payment-provider degradation**

A simulated payment service begins experiencing elevated errors and latency
because its primary third-party payment provider becomes degraded.

---

## MVP Workflow

```text
Incident Trigger
      |
      v
Incident Created
      |
      v
Evidence Collection
      |
      +--> Service Health
      +--> Logs
      +--> Deployment History
      +--> Runbooks
      +--> Historical Incidents
      |
      v
AI Investigation
      |
      v
Root Cause Hypothesis
      |
      v
Remediation Recommendation
      |
      v
Human Approval
      |
      v
Simulated Provider Failover
      |
      v
Recovery Verification
      |
      v
Incident Resolution
```

---
## Included Capabilities

### Incident Management
- create incidents,
- retrieve incidents,
- update incident status,
- retain incident history.
### Operational Tools
- retrieve service health,
- retrieve logs,
- retrieve deployment history,
- inspect service configuration.
### Knowledge Retrieval
- runbooks,
- historical incidents.
### AI Investigation
- structured root-cause hypothesis,
- evidence references,
- confidence metadata,
- recommended remediation.
### Remediation
- approval requirement,
- simulated payment-provider failover,
- recovery verification.
### Audit
- user action,
- agent action,
- tool invocation,
- approval event,
- remediation execution.
---

---
## Explicitly Deferred

### The following are outside MVP scope:
- Kubernetes operations,
- real cloud-provider integration,
- real production credentials,
- automatic production rollback,
- Slack integration,
- PagerDuty integration,
- Jira integration,
- multi-tenant billing,
- mobile application.


---