# TimeBite
Previously called CYRA (Creating Your Reality Agent), TimeBite is an Apple Vision Claw-style productivity agent with a measurable eval/benchmark loop for computer-use tasks.

![TimeBite Logo](assets/TimeBite.png)

## TL;DR
TimeBite captures user intent (voice/text), plans safe computer actions, runs guarded execution loops, and reports time-reclaimed outcomes through dashboard metrics and benchmark runs.

## Product Goals
- Build an iOS-first agentic productivity experience.
- Enforce safe execution with policy checks and human approvals.
- Benchmark reliability under perturbations (popups, layout shifts, out-of-stock states).
- Quantify value through `minutes_reclaimed` and scenario success metrics.

## AgentBeats Integration (From CYRA Repo)
- Source benchmark repo: [CYRA-AgentBeatsHackathon](https://github.com/erinjerri/CYRA-AgentBeatsHackathon)
- Current CYRA green image: `ghcr.io/erinjerri/cyra-green-agent:latest`
- Demo: [YouTube walkthrough](https://youtu.be/RiCsyp49Qn0)
- Agent profile: [AgentBeats - Create Your Reality](https://agentbeats.dev/erinjerri/create-your-reality)

### Evaluation Status
- CYRA is already registered as a Green Agent with a baseline Purple Agent.
- Leaderboard/eval pipeline is configured in the CYRA repo.
- TimeBite extends the same architecture for productivity and time-reclaimed benchmarking.

### Running Green Agent Container
```bash
docker pull ghcr.io/erinjerri/cyra-green-agent:latest
docker run ghcr.io/erinjerri/cyra-green-agent:latest
```

### After Running Agents (Recommended Flow)
1. Validate run logs and output artifacts (success/failure + telemetry).
2. Update `scenario.toml` participant IDs/env in the leaderboard repo.
3. Trigger assessment workflow from a branch and review generated results.
4. Merge results PR to publish leaderboard updates.
5. Sync key metrics into TimeBite dashboard docs (`minutes_reclaimed`, success rate, unsafe action rate).

### Reuse vs New Docker Image / Agent Registration
- Reuse existing CYRA Green Agent if evaluator contract and benchmark scope are unchanged.
- Publish a new image tag if logic changed (policy, scoring, tool behavior, schema), then update the registered agent image reference.
- Register a new Green Agent only if you are creating a distinct benchmark identity (new domain/leaderboard), not for routine iteration.

## Information Architecture
```mermaid
flowchart TD
    A["User Intent (Voice/Text)"] --> B["Intent Normalizer"]
    B --> C["Task/Session Orchestrator"]
    C --> D["Policy + Guardrails"]
    D --> E["Agent Runtime (Plan -> Act -> Observe)"]
    E --> F["Computer Use Layer (Screenshot/OCR/Action)"]
    E --> G["Approval Gate (cart/checkout/irreversible)"]
    F --> H["Telemetry Stream"]
    G --> H
    H --> I["Run/Event Storage"]
    I --> J["Insights Engine"]
    J --> K["Dashboard (Ring, Buckets, Matrix)"]
    I --> L["Benchmark Harness"]
    L --> M["Reliability Report"]
```

## System Design
```mermaid
flowchart LR
    subgraph Client["Client Layer"]
        C1["iOS App"]
        C2["Dashboard UI"]
    end

    subgraph API["Backend/API Layer"]
        A1["/process"]
        A2["/runs"]
        A3["/metrics"]
        A4["Policy Service"]
        A5["Approval Service"]
    end

    subgraph Runtime["Agent Runtime Layer"]
        R1["Planner"]
        R2["Vision/OCR Context"]
        R3["Action Executor"]
        R4["Retry + Timeout Controller"]
    end

    subgraph Data["Data Layer"]
        D1["Task Store"]
        D2["Session/Run Store"]
        D3["Event Logs"]
        D4["Insight Aggregates"]
    end

    C1 --> A1
    C1 --> A2
    C2 --> A3
    A1 --> A4
    A1 --> R1
    R1 --> R2
    R2 --> R3
    R3 --> R4
    R4 --> A5
    R4 --> D3
    A2 --> D2
    A3 --> D4
    A1 --> D1
    D3 --> D4
```

## Agent Loop (Execution + Safety)
```mermaid
sequenceDiagram
    participant U as User
    participant App as iOS App
    participant API as Process API
    participant Policy as Guardrails
    participant Agent as Runtime Loop
    participant Vision as Vision/OCR
    participant Exec as Action Executor
    participant Approve as Human Approval
    participant Log as Telemetry

    U->>App: Submit goal (voice/text)
    App->>API: POST /process
    API->>Policy: Validate allowlist, max-step, timeout
    Policy-->>API: Policy decision
    API->>Agent: Start run(session_id)
    loop Until done or timeout
        Agent->>Vision: Capture screenshot + context
        Vision-->>Agent: Parsed state
        Agent->>Exec: Next safe action
        Exec-->>Agent: Outcome
        Agent->>Log: step(action, latency, outcome)
        alt Irreversible action detected
            Agent->>Approve: Request confirmation
            Approve-->>Agent: Approve/Reject
        end
    end
    Agent-->>API: Final run result + summary
    API-->>App: Response + insights
```

## Planned API Surface
| Endpoint | Method | Purpose |
|---|---|---|
| `/process` | `POST` | Start/continue an agent run from structured intent. |
| `/runs` | `GET` | Fetch run history, statuses, and scenario results. |
| `/metrics` | `GET` | Return dashboard metrics (time reclaimed, reliability, safety). |

## Core Data Model (Planned)
| Entity | Key Fields |
|---|---|
| `Task` | `task_id`, `intent`, `constraints`, `priority`, `created_at` |
| `Session` | `session_id`, `user_id`, `start_time`, `end_time`, `status` |
| `Run` | `run_id`, `session_id`, `scenario`, `score`, `duration_ms`, `result` |
| `Insight` | `insight_id`, `session_id`, `minutes_reclaimed`, `bucket`, `created_at` |
| `StepEvent` | `run_id`, `step_index`, `action`, `latency_ms`, `outcome`, `safety_flag` |

## Safety and Compliance Defaults
- Allowlist-based action policy.
- Max steps per run and strict wall-clock timeout.
- Mandatory human confirmation for checkout/cart/final submit.
- Benchmark-time perturbation tests before release freeze.

## Metrics That Matter
- `minutes_reclaimed` per run/day/week.
- Success rate across scored benchmark sessions.
- Unsafe action rate under perturbation.
- Median latency per action and end-to-end run time.

## Quick Start (Boilerplate)
```bash
# 1) Clone
git clone https://github.com/erinjerri/TimeBite.git
cd TimeBite

# 2) Create env file (example)
cp .env.example .env

# 3) Install deps
# npm install

# 4) Run app/api
# npm run dev
```

> Note: this repository is currently documentation-first. Replace placeholder setup commands with your actual stack commands as implementation lands.

## Documentation
- Roadmap checklist: [docs/to-do-list.md](docs/to-do-list.md) (also embedded below).
- Architecture and safety baseline: this README.
