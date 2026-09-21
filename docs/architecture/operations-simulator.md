# Operations Simulator

## Purpose

The SentinelAI Operations Simulator provides a deterministic,
non-production environment for testing AI-driven incident investigation
and remediation workflows.

It allows SentinelAI to interact with realistic operational evidence
without requiring access to real production infrastructure.

## Simulated Organization

The MVP represents a fictional payment platform named NovaPay.

The primary service under investigation is:

`payment-service`

The service communicates with two external payment providers:

- GlobalPay — primary provider
- PayFlow — backup provider

## Normal State

Under normal operating conditions:

- service status is healthy,
- error rate is approximately 0.4%,
- P95 latency is approximately 380 ms,
- CPU and memory usage are normal,
- database latency is normal,
- GlobalPay is the active provider.

## Provider Degradation Scenario

The provider-degradation scenario simulates elevated latency from
GlobalPay.

During the scenario:

- payment error rate rises,
- P95 latency rises significantly,
- PaymentProviderTimeout errors appear,
- circuit-breaker warnings appear,
- CPU remains relatively normal,
- memory remains relatively normal,
- database latency remains relatively normal.

These signals allow later AI investigation components to distinguish
external dependency failure from internal resource exhaustion.

## Recovery

The simulated remediation action switches payment traffic from GlobalPay
to PayFlow.

After failover:

- service status returns to healthy,
- error rate decreases,
- P95 latency decreases,
- PayFlow becomes the active provider.

## Safety

The simulator does not interact with real infrastructure.

All operational changes are maintained entirely within SentinelAI's
in-memory simulation state during the MVP.

## Future Evolution

The simulator interfaces are intentionally separated from future agent
logic.

This allows simulated operations to later be replaced or supplemented by:

- REST integrations,
- observability systems,
- cloud infrastructure APIs,
- MCP servers,
- WSO2-governed enterprise tools.