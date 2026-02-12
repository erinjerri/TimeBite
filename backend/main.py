from __future__ import annotations

import csv
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"
TASKS_CSV = DATA_DIR / "master_tasks.csv"
INSIGHTS_CSV = DATA_DIR / "timecake_insights.csv"
TELEMETRY_DIR = DATA_DIR / "telemetry_runs"

app = FastAPI(title="TimeBite API", version="0.1.0")


class ProcessPayload(BaseModel):
    task_id: str | None = None
    title: str
    intent_text: str | None = None
    source_modality: str = "text"
    scenario: str | None = None
    priority: int = Field(default=1, ge=0, le=3)
    session_id: str | None = None
    notes: str | None = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_task_row(payload: ProcessPayload, run_id: str) -> str:
    task_id = payload.task_id or f"TB-{int(time.time())}"
    row = {
        "task_id": task_id,
        "created_at": now_iso(),
        "focus": "Backend",
        "title": payload.title,
        "intent_text": payload.intent_text or "",
        "source_modality": payload.source_modality,
        "scenario": payload.scenario or "",
        "status": "pending",
        "owner": "erinjerri",
        "priority": str(payload.priority),
        "budget_limit": "",
        "max_steps": "",
        "timeout_ms": "",
        "approval_required": "false",
        "minutes_reclaimed": "",
        "session_id": payload.session_id or "",
        "run_id": run_id,
        "notes": payload.notes or "",
    }
    with TASKS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writerow(row)
    return task_id


def append_telemetry_event(run_id: str, event: dict[str, Any]) -> Path:
    TELEM_FILE = TELEMETRY_DIR / f"{run_id}.jsonl"
    TELEM_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TELEM_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    return TELEM_FILE


@app.post("/process")
async def process(payload: ProcessPayload) -> dict[str, Any]:
    run_id = f"R-{uuid.uuid4().hex[:8]}"
    task_id = append_task_row(payload, run_id)
    event = {
        "run_id": run_id,
        "task_id": task_id,
        "session_id": payload.session_id,
        "ts": now_iso(),
        "step_index": 1,
        "action": "process_task",
        "latency_ms": 0,
        "outcome": "accepted",
        "safety_flag": "none",
        "source_modality": payload.source_modality,
        "scenario": payload.scenario,
    }
    telem_path = append_telemetry_event(run_id, event)
    return {"status": "accepted", "task_id": task_id, "run_id": run_id, "telemetry_file": str(telem_path)}


@app.get("/runs")
async def runs() -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for path in sorted(TELEMETRY_DIR.glob("*.jsonl")):
        line_count = 0
        first_ts = ""
        last_ts = ""
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                line_count += 1
                if line_count == 1:
                    try:
                        first_ts = json.loads(line).get("ts", "")
                    except json.JSONDecodeError:
                        first_ts = ""
                try:
                    last_ts = json.loads(line).get("ts", last_ts)
                except json.JSONDecodeError:
                    pass
        items.append(
            {
                "run_id": path.stem,
                "events": line_count,
                "first_ts": first_ts,
                "last_ts": last_ts,
                "file": str(path),
            }
        )
    return {"count": len(items), "runs": items}


@app.get("/metrics")
async def metrics() -> dict[str, Any]:
    total_minutes = 0.0
    rows = 0
    if INSIGHTS_CSV.exists():
        with INSIGHTS_CSV.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows += 1
                try:
                    total_minutes += float(row.get("metric_value") or 0)
                except ValueError:
                    continue
    return {
        "insight_rows": rows,
        "minutes_reclaimed_total": round(total_minutes, 2),
        "run_files": len(list(TELEMETRY_DIR.glob("*.jsonl"))),
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "timebite-api"}
