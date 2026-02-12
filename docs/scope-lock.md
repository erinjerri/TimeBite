# Thu Feb 12 - Scope Lock (iOS-first MVP)

## Objective
Lock the MVP scope and define novelty as a measurable `minutes_reclaimed` benchmark.

## In Scope (MVP)
- iOS-first intent capture (voice/text).
- Structured action request generation.
- Safe agent loop (`plan -> act -> observe`) with retries.
- Human approval for cart/checkout/irreversible actions.
- Telemetry logging per step (`action`, `latency_ms`, `outcome`, `safety_flag`).
- Dashboard basics:
  - Reverse day timer ring.
  - Minutes reclaimed metric.
  - Basic insight buckets (personal/professional/sleep).

## Out of Scope (Post-MVP)
- Multi-platform clients beyond iOS.
- Full production auth/multi-tenant RBAC.
- Advanced personalization or long-term memory optimization.
- Large partner integrations unless required for demo.

## Novelty Definition
TimeBite novelty is demonstrated by measured time reclaimed while maintaining safety:
- `minutes_reclaimed` > baseline manual-flow time.
- No unsafe irreversible actions without explicit human approval.
- Reliable completion across benchmark scenarios with perturbations.

## Acceptance Criteria
- `docs/scope-lock.md` reviewed and accepted.
- At least 3 benchmark scenarios selected for MVP.
- Baseline measurement method documented for `minutes_reclaimed`.
- Policy guardrail defaults defined (allowlist, max-step, timeout, approval gate).

## Scenario Set (Initial)
- Retail: "Mom gift scenario" with 3-item target.
- Food compare: DoorDash/Grubhub/Yelp stub flow.
- Reliability stress: popup/layout/out-of-stock perturbation case.

## Notes
- Reuse existing registered Green Agent unless benchmark identity changes.
- New image tags are sufficient for iteration; new registration is optional and only for distinct leaderboard identity.

