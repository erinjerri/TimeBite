# Task Schema v2 (TimeBite)

Based on CYRA `TaskPayload` + `TaskOut`, adapted for TimeBite productivity benchmarking, CoreML context, and safety gating.

## Design Goals
- Keep compatibility with CYRA task basics (`id`, `title`, `priority`, `status`, `task`).
- Add structured fields needed for reproducible runs and `minutes_reclaimed`.
- Add explicit safety and approval fields for irreversible actions.

## JSON Shape

### Required
- `task_id` (string): stable identifier (UUID or timestamp-based ID).
- `title` (string): short user-facing task name.
- `status` (string enum): `planned | pending | running | blocked | completed | failed | cancelled`.
- `priority` (integer): `0-3` where `0` is lowest, `3` highest.
- `created_at` (string): ISO-8601 timestamp.

### Optional
- `intent_text` (string): normalized user intent.
- `source_modality` (string enum): `voice | text | coreml_vision | mixed`.
- `scenario` (string): benchmark scenario key (for example `mom-gift-v1`).
- `constraints` (object):
  - `budget_limit` (number)
  - `categories` (array of strings)
  - `max_steps` (integer)
  - `timeout_ms` (integer)
- `policy` (object):
  - `allowlist_id` (string)
  - `approval_required` (boolean)
  - `irreversible_action_types` (array of strings)
- `assignment` (object):
  - `owner` (string)
  - `session_id` (string)
  - `run_id` (string)
- `metrics` (object):
  - `baseline_minutes` (number)
  - `actual_minutes` (number)
  - `minutes_reclaimed` (number)
- `coreml_context` (object):
  - `model` (string)
  - `confidence` (number)
  - `observations` (array of strings)
- `notes` (string)
- `updated_at` (string): ISO-8601 timestamp.

## Minimal Example
```json
{
  "task_id": "TB-2026-02-13-001",
  "title": "Find 3 gift options for mom",
  "status": "pending",
  "priority": 2,
  "created_at": "2026-02-13T10:00:00Z"
}
```

## Full Example
```json
{
  "task_id": "TB-2026-02-13-001",
  "title": "Find 3 gift options for mom under $100",
  "status": "running",
  "priority": 2,
  "created_at": "2026-02-13T10:00:00Z",
  "updated_at": "2026-02-13T10:01:32Z",
  "intent_text": "buy a birthday gift for my mom",
  "source_modality": "mixed",
  "scenario": "mom-gift-v1",
  "constraints": {
    "budget_limit": 100.0,
    "categories": ["gifts", "home"],
    "max_steps": 30,
    "timeout_ms": 120000
  },
  "policy": {
    "allowlist_id": "allowlist-v1",
    "approval_required": true,
    "irreversible_action_types": ["checkout", "purchase"]
  },
  "assignment": {
    "owner": "erinjerri",
    "session_id": "S-001",
    "run_id": "R-001"
  },
  "metrics": {
    "baseline_minutes": 18.0,
    "actual_minutes": 7.0,
    "minutes_reclaimed": 11.0
  },
  "coreml_context": {
    "model": "VisionIntent-v1",
    "confidence": 0.92,
    "observations": ["gift category page visible", "price filter available"]
  },
  "notes": "Requires approval before checkout."
}
```

## CSV Mapping (master_tasks.csv)
- `task_id`, `created_at`, `focus`, `title`, `intent_text`, `source_modality`, `scenario`, `status`, `owner`, `priority`, `budget_limit`, `max_steps`, `timeout_ms`, `approval_required`, `minutes_reclaimed`, `session_id`, `run_id`, `notes`

