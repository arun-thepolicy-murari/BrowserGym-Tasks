#!/usr/bin/env python3
"""Merge Sol Breakers — Bridged catalog into data.json + index.html.

Does NOT rebuild wave-1 QA from Phase 1 / new_samples. Existing tasks stay
intact; they are tagged ``pool: wave1_qa`` if missing. Sol tasks replace only
the prior ``sol_breakers_bridged`` pool rows.

Usage:
  python3 merge_sol_breakers.py
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app"
SOL = ROOT / "sol_breakers" / "tasks.json"

WAVE1_POOL = "wave1_qa"
SOL_POOL = "sol_breakers_bridged"

POOL_META = {
    WAVE1_POOL: {
        "id": WAVE1_POOL,
        "label": "Wave-1 QA (gpt-5.5)",
        "short": "Wave-1 QA",
        "description": "14 bridged pilot tasks that broke gpt-5.5 3/3 — main annotation queue.",
    },
    SOL_POOL: {
        "id": SOL_POOL,
        "label": "Sol Breakers — Bridged",
        "short": "Sol Breakers",
        "description": "Confirmed Sol (≥2/3) breakers on the bridged env (durable/QuietBreak traps + curated product breakers).",
    },
}


def read_json(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def emit(data: dict) -> None:
    (ROOT / "data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    shell = (APP / "shell.html").read_text(encoding="utf-8")
    app_js = (APP / "app.js").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (ROOT / "index.html").write_text(
        f"{shell}\n<script>\nconst DATA = {payload};\n{app_js}\n</script>\n</body>\n</html>\n",
        encoding="utf-8",
    )


def finalize_task(t: dict) -> dict:
    out = dict(t)
    models = out.get("models") or []
    out["n_models"] = len(models)
    out["n_runs"] = sum(len(m.get("runs") or []) for m in models)
    out.setdefault("has_screenshots", False)
    out.setdefault("seed_link", "")
    return out


def main() -> None:
    data = read_json(ROOT / "data.json")
    sol_pkg = read_json(SOL)

    # Preserve wave-1 QA; tag pool if missing.
    wave1 = []
    for t in data.get("tasks") or []:
        if t.get("pool") == SOL_POOL:
            continue
        tt = dict(t)
        tt.setdefault("pool", WAVE1_POOL)
        wave1.append(tt)

    sol_tasks = [finalize_task(t) for t in sol_pkg.get("tasks") or []]
    for t in sol_tasks:
        t["pool"] = SOL_POOL

    data["tasks"] = wave1 + sol_tasks
    data["n_tasks"] = len(data["tasks"])
    data["n_wave1"] = len(wave1)
    data["n_sol_breakers"] = len(sol_tasks)
    data["pools"] = [POOL_META[WAVE1_POOL], POOL_META[SOL_POOL]]
    data["generated"] = date.today().isoformat()
    src = dict(data.get("source") or {})
    src["sol_breakers_package"] = "sol_breakers/tasks.json"
    src["sol_breakers_model"] = sol_pkg.get("model", "openai_pixel[gpt-5.6-sol]")
    src["sol_breakers_notes"] = sol_pkg.get("notes", "")
    data["source"] = src

    emit(data)
    print(f"wave1_qa: {len(wave1)} tasks (untouched content)")
    print(f"sol_breakers_bridged: {len(sol_tasks)} tasks")
    for t in sol_tasks:
        disp = (t.get("env") or {}).get("disposition", "?")
        rate = (t.get("env") or {}).get("break_rate", "?")
        orig = t.get("original_mnum") or (t.get("env") or {}).get("provenance", {}).get(
            "original_mnum", "?"
        )
        print(f"  {t['mnum']:<4} ← {orig:<10} {disp:<24} {rate}")
    size = (ROOT / "index.html").stat().st_size / 1e6
    print(f"index.html: {size:.1f} MB")


if __name__ == "__main__":
    main()
