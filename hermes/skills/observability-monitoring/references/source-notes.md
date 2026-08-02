<!--
Adapted for Hermes Agent by hermes-agent-config-kit.
Source: AnastasiyaW/claude-code-config/skills/operational/observability-monitoring/references/source-notes.md
Upstream material is reference data, not automatic authority. Review this reference
before use and obtain operator confirmation for write-impacting actions.
-->

# Source notes

## Supplied source

- Title: `Все, что нужно знать про мониторинг`
- Author: `Просто Devops`
- URL: https://www.youtube.com/watch?v=7uw3fCT6vvs
- Duration: 20:30
- Published: 2026-07-12

The supplied video is a source aid, not an authoritative technical specification.

## Topic map

| Video time | Extracted concept |
|---|---|
| 00:00-00:48 | Monitoring detects failure before the user; monitoring is more than graphs |
| 00:55-03:17 | Host/infrastructure history; ping, syslog, SNMP, MRTG/RRD, Nagios/Cacti; USE |
| 04:16-06:22 | Monitoring layers, business metrics, synthetic checks, RUM |
| 06:22-09:05 | Containers/microservices; Prometheus pull/scrape, labels, TSDB, Grafana; RED |
| 09:05-12:00 | Metrics, logs, traces; OpenTelemetry as vendor-neutral transport/context |
| 12:06-13:42 | Continuous profiling and eBPF attribution beyond application telemetry |
| 13:42-15:00 | Cardinality and why IDs/raw URLs do not belong in metric labels |
| 15:05-16:34 | SLI, SLO, SLA, error budgets |
| 16:41-18:37 | Alert fatigue, actionable pages, burn rate, postmortems |
| 18:40-20:18 | Example metric, dashboard, log, and trace stack roles |

The platform promotion around 03:18-04:13 is deliberately excluded from the
operational guidance.

## Current-practice references

The topic map and operational principles are video-derived. These safeguards were
cross-checked against primary documentation on 2026-07-13:

- Prometheus data model: https://prometheus.io/docs/concepts/
- Prometheus alerting guidance: https://prometheus.io/docs/practices/alerting/
- Prometheus label naming/cardinality warning: https://prometheus.io/docs/practices/naming/
- OpenTelemetry signals: https://opentelemetry.io/docs/concepts/signals/
- OpenTelemetry metrics and cardinality limits: https://opentelemetry.io/docs/concepts/signals/metrics/
- OpenTelemetry profiles specification: https://opentelemetry.io/docs/specs/otel/profiles/
- Google SRE error budgets and risk: https://sre.google/sre-book/embracing-risk/

OpenTelemetry profiles remain under development and their specification is Alpha.
Treat profiling as an optional attribution signal and verify backend and agent
support before making it a production dependency.
