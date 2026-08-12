#!/usr/bin/env python3
"""Merge Sol Breakers + Phase 2 + Eligible + Breaker-1 into data.json + index.html.

Does NOT rebuild wave-1 QA from Phase 1 / new_samples. Existing wave-1 tasks stay
intact; they are tagged ``pool: wave1_qa`` if missing. Sol / Phase-2 / Eligible /
Breaker-1 pools replace only their own prior rows.

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
PHASE2 = ROOT / "phase2_dual_breakers" / "tasks.json"
ELIGIBLE = ROOT / "eligible_task_suite" / "tasks.json"
BREAKER1 = ROOT / "breaker1" / "tasks.json"

WAVE1_POOL = "wave1_qa"
SOL_POOL = "sol_breakers_bridged"
PHASE2_POOL = "phase2_dual_breakers"
ELIGIBLE_POOL = "eligible_task_suite"
BREAKER1_POOL = "breaker_1"

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
    PHASE2_POOL: {
        "id": PHASE2_POOL,
        "label": "Filtration 21/47 — Dual Breakers",
        "short": "Filtration 21/47",
        "description": "Tencent filtration Phase 2 dual filtration fails after refuse-credit fix + Opus credit re-audit (Sol + Opus both ≥2/5 on valid seeds). Of 21: 9 dual-trap-hit, 11 Sol-trap/Opus-refuse, 1 ambiguous (M210). Sample20 9/20 + Remaining27 12/27. Left-dual: refuse-credit M39/M40/M213/M220 + credit-death M103/M104/M227; M117 stays.",
    },
    ELIGIBLE_POOL: {
        "id": ELIGIBLE_POOL,
        "label": "Eligible Task Suite",
        "short": "Eligible Suite",
        "description": "Sol breaker eligibility candidates with full step screenshot galleries (e1–e13: mail_002, md_002, mp_040/048/053/056/058–064). Verifier panel includes What it requires / What the agent did. Breakers-only (no mp_065 / nine-mech HOLDs).",
    },
    BREAKER1_POOL: {
        "id": BREAKER1_POOL,
        "label": "Breaker-1",
        "short": "Breaker-1",
        "description": "b1 mp_091 Burrow pickup BREAK + b2 mp_096 Lumos QuietBreak + b3 mp_111 + b4 mp_112 + b5 mp_119 + b6 mp_120 + b7 mp_092 Leroy helmet + b8 mp_093 cancelled lunch + b9–b13 mp_123/124/125/127/128 fact-probe BREAKs. Dropped: mp_104 FN, mp_113 twin, mp_114/115 fairness HOLDs, mp_116 ambiguous, mp_118 unconfirmed. Full trajectory galleries.",
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
    phase2_pkg = read_json(PHASE2) if PHASE2.exists() else {"tasks": []}
    eligible_pkg = read_json(ELIGIBLE) if ELIGIBLE.exists() else {"tasks": []}
    breaker1_pkg = read_json(BREAKER1) if BREAKER1.exists() else {"tasks": []}

    # Preserve wave-1 QA; drop prior sol + phase2 + eligible + breaker1 rows.
    wave1 = []
    for t in data.get("tasks") or []:
        p = t.get("pool") or WAVE1_POOL
        if p in (SOL_POOL, PHASE2_POOL, ELIGIBLE_POOL, BREAKER1_POOL):
            continue
        tt = dict(t)
        tt.setdefault("pool", WAVE1_POOL)
        wave1.append(tt)

    sol_tasks = [finalize_task(t) for t in sol_pkg.get("tasks") or []]
    for t in sol_tasks:
        t["pool"] = SOL_POOL

    phase2_tasks = [finalize_task(t) for t in phase2_pkg.get("tasks") or []]
    for t in phase2_tasks:
        t["pool"] = PHASE2_POOL

    eligible_tasks = [finalize_task(t) for t in eligible_pkg.get("tasks") or []]
    for t in eligible_tasks:
        t["pool"] = ELIGIBLE_POOL

    breaker1_tasks = [finalize_task(t) for t in breaker1_pkg.get("tasks") or []]
    for t in breaker1_tasks:
        t["pool"] = BREAKER1_POOL

    data["tasks"] = wave1 + sol_tasks + phase2_tasks + eligible_tasks + breaker1_tasks
    data["n_tasks"] = len(data["tasks"])
    data["n_wave1"] = len(wave1)
    data["n_sol_breakers"] = len(sol_tasks)
    data["n_phase2_dual"] = len(phase2_tasks)
    data["n_eligible_suite"] = len(eligible_tasks)
    data["n_breaker1"] = len(breaker1_tasks)
    data["pools"] = [
        POOL_META[WAVE1_POOL],
        POOL_META[SOL_POOL],
        POOL_META[PHASE2_POOL],
        POOL_META[ELIGIBLE_POOL],
        POOL_META[BREAKER1_POOL],
    ]
    data["generated"] = date.today().isoformat()
    src = dict(data.get("source") or {})
    src["sol_breakers_package"] = "sol_breakers/tasks.json"
    src["sol_breakers_model"] = sol_pkg.get("model", "openai_pixel[gpt-5.6-sol]")
    src["sol_breakers_notes"] = sol_pkg.get("notes", "")
    src["phase2_dual_package"] = "phase2_dual_breakers/tasks.json"
    src["phase2_dual_headline"] = phase2_pkg.get("headline", "")
    src["phase2_dual_notes"] = phase2_pkg.get("notes", "")
    src["eligible_task_suite_package"] = "eligible_task_suite/tasks.json"
    src["eligible_task_suite_notes"] = eligible_pkg.get("notes", "")
    src["breaker1_package"] = "breaker1/tasks.json"
    src["breaker1_notes"] = breaker1_pkg.get("notes", "")
    data["source"] = src
    data["phase2_meta"] = {
        "headline": phase2_pkg.get("headline"),
        "pool_outcomes": phase2_pkg.get("pool_outcomes"),
        "bar": phase2_pkg.get("bar"),
        "panels": phase2_pkg.get("panels"),
        "inconclusive_not_shown": phase2_pkg.get("inconclusive_not_shown"),
        "models": phase2_pkg.get("models"),
        "behavior_retag": phase2_pkg.get("behavior_retag"),
        "notes": phase2_pkg.get("notes"),
    }
    data["eligible_meta"] = {
        "headline": eligible_pkg.get("label") or "Eligible Task Suite",
        "notes": eligible_pkg.get("notes"),
        "model": eligible_pkg.get("model"),
    }
    data["breaker1_meta"] = {
        "headline": breaker1_pkg.get("label") or "Breaker-1",
        "notes": breaker1_pkg.get("notes"),
        "model": breaker1_pkg.get("model"),
    }

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
    print(f"phase2_dual_breakers: {len(phase2_tasks)} tasks")
    for t in phase2_tasks:
        e = t.get("env") or {}
        print(
            f"  {t['mnum']:<5} {t.get('panel','?'):<12} "
            f"Sol {e.get('sol_fail_rate','?')} · Opus {e.get('opus_fail_rate','?')}"
        )
    print(f"eligible_task_suite: {len(eligible_tasks)} tasks")
    for t in eligible_tasks:
        e = t.get("env") or {}
        print(
            f"  {t['mnum']:<4} ← {(t.get('original_mnum') or '?'):<10} "
            f"{e.get('disposition','?'):<8} score={(t.get('models') or [{}])[0].get('runs',[{}])[0].get('score','?')} "
            f"steps={(t.get('models') or [{}])[0].get('runs',[{}])[0].get('true_n_steps','?')}"
        )
    print(f"breaker_1: {len(breaker1_tasks)} tasks")
    for t in breaker1_tasks:
        e = t.get("env") or {}
        print(
            f"  {t['mnum']:<4} ← {(t.get('original_mnum') or '?'):<10} "
            f"{e.get('disposition','?'):<8} score={(t.get('models') or [{}])[0].get('runs',[{}])[0].get('score','?')} "
            f"steps={(t.get('models') or [{}])[0].get('runs',[{}])[0].get('true_n_steps','?')}"
        )
    size = (ROOT / "index.html").stat().st_size / 1e6
    print(f"index.html: {size:.1f} MB")


if __name__ == "__main__":
    main()
