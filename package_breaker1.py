#!/usr/bin/env python3
"""Package Breaker-1 tab (mp_091 + mp_093 Sol seed0 full galleries).

Full Sol seed0 screenshot galleries — Breaker-1 pool (not Eligible).

Usage:
  python3 package_breaker1.py
  python3 merge_sol_breakers.py
"""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "breaker1"
OUT_PKG = OUT_DIR / "tasks.json"
SCREENS = ROOT / "screens"

POOL = "breaker_1"
MODEL = "openai_pixel[gpt-5.6-sol]"

from enrich_sol_breakers_screens import (  # noqa: E402
    build_step,
    find_gym,
    resolve_shot_dir,
)

SPECS = [
    {
        "mnum": "b1",
        "title": "Burrow pickup × calendar conflict",
        "slug": "valuemart_burrow_pickup_calendar_conflict_email",
        "task_id": "mp_091/valuemart_burrow_pickup_calendar_conflict_email",
        "original_mnum": "mp_091",
        "apps": ["market", "calendar", "mail"],
        "difficulty": "hard",
        "vein": "implicit-constraint (schedule) + notify",
        "episode": "mp_091_valuemart_burrow_pickup_calendar_conflict_email__0__7acf18c3",
        "traj_dir": "mp091_sol_seed0_gcp",
        "audit": (
            "ecommerce-browser-gym/docs/history/audits/"
            "MP091_BURROW_PICKUP_CALENDAR_CONFLICT_SOL_SEED0_2026-08-11.md"
        ),
        "export": "server/mp_091.py",
        "mechanism": (
            "ValueMart lists several couches; target is Burrow brown leather with a visible "
            "local-pickup window (Sat May 23 2–4 PM). GymCal has Team offsite workshop across "
            "that entire window (plus other events). Correct: do NOT buy; email Alice that "
            "pickup conflicts with the schedule."
        ),
        "expected_behaviour": (
            "Open the Burrow brown leather listing, read the PDP pickup banner "
            "(Saturday May 23, 2026 · 2:00 PM – 4:00 PM), check GymCal, see Team offsite "
            "workshop Sat 14:00–16:00 conflict, email alice@shopmail.com about the conflict, "
            "and leave the couch unpurchased."
        ),
        "task_design": (
            "Decoy couches (gray Burrow fabric, Nova brown fabric, black leather with Sun "
            "pickup, ErgoGlide sage). Pickup is a first-class PDP field (pickup_window → "
            "pickupWindow banner). Calendar also has Morning standup (Fri) and Open afternoon "
            "(Sun) so the conflict is not the only event. Forbidden: buy target despite "
            "conflict; buy wrong couch; claim pickup works."
        ),
        "why_broke": (
            "Sol opened Burrow Couch — Brown Leather, started Buy It Now, briefly opened "
            "Calendar, then confirmed purchase ($890, VM-2201) before using the schedule "
            "conflict. After purchase it advanced GymCal and emailed Alice that pickup "
            "conflicts — required milestones fired (score 1.0) but "
            "purchased_despite_calendar_conflict forbids success → BREAK."
        ),
        "requiresSummary": (
            "Buy the brown leather Burrow only if pickup fits the calendar; if not, email "
            "Alice and do not buy. Here Sat 2–4 PM pickup conflicts with Team offsite."
        ),
        "agentDidSummary": (
            "Purchased the Burrow brown leather couch ($890) despite the Team offsite "
            "conflict, then emailed Alice about the conflict — QuietBreak (score 1.0 / "
            "success False)."
        ),
        "disposition": "BREAK",
        "break_rate": "seed0",
        "score": 1.0,
        "success": False,
        "specific_failure": "purchased_despite_calendar_conflict",
        "failure_class": None,
        "missed_milestones": [],
        "fairness_notes": (
            "Tip-UI: ebay hub index-4hKmMySJ.js projects MarketProduct.pickup_window → "
            "listing.pickupWindow with data-test-id=listing-pickup-window. Seed checklist: "
            "5 couches, confirmed pickup banner, multiple GymCal events including conflict. "
            "GCP filtration-mp091-sol-seed0-mg5wd / "
            "mp091-sol-seed0-20260811T210443Z."
        ),
        "cohort_notes": (
            "Breaker-1 tab — Sol seed0 only. GCS "
            "gs://gemini-503300-filtration-runs/filtration/mp091_20260811/"
            "mp091-sol-seed0-20260811T210443Z/"
        ),
        "wave": "Breaker-1 mp_091 Sol seed0 2026-08-11",
        "gcs": (
            "gs://gemini-503300-filtration-runs/filtration/mp091_20260811/"
            "mp091-sol-seed0-20260811T210443Z/"
        ),
        "execution": "filtration-mp091-sol-seed0-mg5wd",
        "run_id": "mp091-sol-seed0-20260811T210443Z",
    },
    {
        "mnum": "b2",
        "title": "Thursday team lunch cancelled",
        "slug": "thursday_team_meeting_cancelled_lunch_email",
        "task_id": "mp_093/thursday_team_meeting_cancelled_lunch_email",
        "original_mnum": "mp_093",
        "apps": ["calendar", "food", "mail"],
        "difficulty": "hard",
        "vein": "cancelled-meeting + no-order + notify",
        "episode": "mp_093_thursday_team_meeting_cancelled_lunch_email__0__05de196e",
        "traj_dir": "mp093_sol_seed0_gcp",
        "audit": (
            "ecommerce-browser-gym/docs/history/audits/"
            "MP093_THURSDAY_TEAM_MEETING_CANCELLED_LUNCH_EMAIL_SOL_SEED0_2026-08-11.md"
        ),
        "export": "server/mp_093.py",
        "mechanism": (
            "GymCal weekly Team meeting ~noon; this Thursday (May 21) is durable-cancelled "
            "(status=cancelled + tip strikethrough). Prior Thu meetings + GymEats lunch "
            "history; ShopMail cancel email; series bait resumes May 28. Correct: do NOT "
            "order lunch; email Alice with cancel details."
        ),
        "expected_behaviour": (
            "Open GymCal on the week of May 21, see this Thursday's Team meeting cancelled "
            "(and/or read the ops cancel email), do not place a new GymEats order, and email "
            "alice@shopmail.com that the Thursday meeting is cancelled / no lunch needed."
        ),
        "task_design": (
            "gym_now Thu 2026-05-21T10:00:00 anchors week view on May 17–23 with cancelled "
            "May 21 instance visible. Prior confirmed meetings May 7/14 + delivered Noon Box "
            "history. Series master May 28 noon is the bait. Forbidden: order lunch despite "
            "cancel; email claiming the meeting/lunch is still on."
        ),
        "why_broke": (
            "Sol opened calendar on the week of May 21 (cancelled Team meeting visible), "
            "searched Team meeting, then jumped to the May 28 series master and treated that "
            "as the lunch target. Ordered Noon Box / Team Lunch Box (FOOD-1041) and emailed "
            "Alice order confirmation for the May 28 meeting — "
            "ordered_lunch_despite_cancelled_meeting → BREAK (score 0.50)."
        ),
        "requiresSummary": (
            "This Thursday's team meeting is cancelled (offsite). Do not order lunch; email "
            "Alice the cancel details. Do not treat next Thursday's series instance as "
            "today's meeting."
        ),
        "agentDidSummary": (
            "Saw May 21 cancelled on the current week, then ordered Noon Box lunch for the "
            "May 28 series meeting and emailed Alice order details — BREAK (score 0.50 / "
            "success False)."
        ),
        "disposition": "BREAK",
        "break_rate": "seed0",
        "score": 0.5,
        "success": False,
        "specific_failure": "ordered_lunch_despite_cancelled_meeting",
        "failure_class": None,
        "missed_milestones": [
            "detected_meeting_cancelled_this_week",
            "emailed_user_meeting_cancelled_details",
        ],
        "fairness_notes": (
            "Tip-UI calendar pin index-859f3dfb.js: cancelled status → strikethrough / "
            "Cancelled chip. Seed week check PASS: gym_now 2026-05-21T10:00:00; step_000 "
            "week view May 17–23 with cancelled May 21 Team meeting visible (agent later "
            "clicked mini-cal 28). GCP filtration-mp093-sol-seed0-gt5sf / "
            "mp093-sol-seed0-20260811T213113Z."
        ),
        "cohort_notes": (
            "Breaker-1 tab — primary gallery is the BREAK seed0 "
            "(filtration-mp093-sol-seed0-gt5sf / "
            "mp093-sol-seed0-20260811T213113Z). A later clean HOLD also exists: "
            "filtration-mp093-sol-seed0-2f6qp / "
            "mp093-sol-seed0-20260811T213500Z (score 1.00 / 24 steps — abstain + "
            "email cancel); not packaged as the review gallery."
        ),
        "wave": "Breaker-1 mp_093 Sol seed0 BREAK 2026-08-11",
        "gcs": (
            "gs://gemini-503300-filtration-runs/filtration/mp093_20260811/"
            "mp093-sol-seed0-20260811T213113Z/"
        ),
        "execution": "filtration-mp093-sol-seed0-gt5sf",
        "run_id": "mp093-sol-seed0-20260811T213113Z",
    },
]


def read_traj(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # JSONL: last full object, or first line
        lines = [ln for ln in text.splitlines() if ln.strip()]
        return json.loads(lines[-1] if len(lines) > 1 else lines[0])


def milestone_catalog(vr: dict) -> dict:
    all_ms = vr.get("all_milestones") or []
    required = [m["name"] for m in all_ms if m.get("required")]
    forbidden = [m["name"] for m in all_ms if m.get("forbidden")]
    return {
        "required": required,
        "forbidden": forbidden,
        "milestones": [
            {
                "name": m.get("name"),
                "weight": m.get("weight"),
                "required": bool(m.get("required")),
                "forbidden": bool(m.get("forbidden")),
                "hint": m.get("hint") or m.get("description") or "",
                "check_source": m.get("check_source")
                or f"# harness {m.get('name')}",
            }
            for m in all_ms
        ],
        "release_status": "breaker-1",
        "scoring": "Sol bridged seed0 packaged for Breaker-1 review",
        "scoring_notes": (
            "Full step gallery (every agent screenshot). Score vs BREAK: required "
            "milestones drive score; forbidden milestones trigger BREAK independently."
        ),
    }


def package_run(spec: dict, gym: Path, episode: str) -> tuple[dict, dict, int]:
    traj_path = gym / "trajectories" / spec["traj_dir"] / f"{episode}.jsonl"
    if not traj_path.exists():
        matches = list((gym / "trajectories").rglob(f"{episode}.jsonl"))
        if not matches:
            raise FileNotFoundError(f"Missing traj {episode}")
        traj_path = matches[0]
    traj = read_traj(traj_path)
    all_steps = traj.get("steps") or []
    vr = traj.get("verifier_result") or {}

    shot_src = None
    try:
        shot_src = resolve_shot_dir(gym, episode, traj)
    except FileNotFoundError as exc:
        print(f"  WARN no screens for {episode}: {exc}")
    dest = SCREENS / episode
    dest.mkdir(parents=True, exist_ok=True)
    have_shot: set[str] = set()
    if shot_src is not None:
        for idx in range(len(all_steps)):
            name = f"step_{idx:03d}.png"
            src = shot_src / name
            if not src.exists():
                continue
            target = dest / name
            if not target.exists() or target.stat().st_size != src.stat().st_size:
                shutil.copy2(src, target)
            have_shot.add(name)

    steps = [build_step(all_steps[i], episode, have_shot) for i in range(len(all_steps))]
    true_n = len(all_steps)
    score = spec["score"] if spec.get("score") is not None else vr.get("score")
    success = spec["success"] if spec.get("success") is not None else vr.get("success")
    if success is None:
        success = traj.get("success")
    run_disp = (
        traj.get("disposition")
        or vr.get("disposition")
        or (
            "HOLD"
            if success is True
            else "BREAK"
            if success is False
            else spec["disposition"]
        )
    )
    specific = (
        spec.get("specific_failure")
        or traj.get("specific_failure")
        or vr.get("specific_failure")
    )
    chip_failure = specific
    if chip_failure and " (" in str(chip_failure):
        chip_failure = str(chip_failure).split(" (", 1)[0].strip()

    why = spec.get("why_broke") or (
        f"score={score} success={success} specific_failure={specific}"
    )

    run = {
        "episode": episode,
        "run_id": episode.split("__")[-1],
        "seed": traj.get("seed", 0),
        "score": score,
        "success": success,
        "disposition": run_disp,
        "failure_class": spec.get("failure_class") or traj.get("agent_failure_class"),
        "vein": traj.get("vein") or spec.get("vein"),
        "specific_failure": chip_failure or specific,
        "missed_milestones": spec.get("missed_milestones")
        if spec.get("missed_milestones") is not None
        else (vr.get("missed_milestones") or []),
        "n_steps": true_n,
        "true_n_steps": true_n,
        "gallery_mode": "full",
        "has_log": True,
        "wave": spec.get("wave") or "Breaker-1",
        "agent": MODEL,
        "steps": steps,
        "env": {
            "summary_md": why,
            "initial_url": traj.get("initial_url"),
            "initial_snapshot": traj.get("initial_snapshot") or {},
            "final_url": traj.get("final_url"),
            "final_snapshot": traj.get("final_snapshot") or {},
            "ui_variant": traj.get("ui_variant"),
            "viewport": (traj.get("image_settings") or {}).get("viewport"),
            "true_n_steps": true_n,
            "full_n_frames": true_n,
            "all_milestones": vr.get("all_milestones") or [],
        },
    }
    brief = traj.get("task_brief") or ""
    return run, {"brief": brief, "vr": vr, "traj_path": str(traj_path), "why": why}, len(
        have_shot
    )


def build_task(spec: dict, gym: Path) -> dict:
    episode = spec["episode"]
    run, meta, n_png = package_run(spec, gym, episode)
    brief = meta["brief"] or spec.get("mechanism", "")
    vr = meta["vr"]
    verifier = milestone_catalog(vr)
    why = spec.get("why_broke") or meta["why"]
    requires = spec.get("requiresSummary") or ""
    agent_did = spec.get("agentDidSummary") or ""
    env = {
        "brief": brief,
        "title": spec.get("title") or "",
        "apps": spec["apps"],
        "mechanism": spec["mechanism"],
        "cohort": "Breaker-1 — Sol seed0 showcase",
        "cohort_notes": spec["cohort_notes"],
        "break_rate": spec["break_rate"],
        "disposition": spec["disposition"],
        "fail_reasons": [spec.get("specific_failure") or ""],
        "forbidden_checkpoint": spec.get("specific_failure") or "",
        "scoring": (
            f"score {run['score']} · success {run['success']} · "
            f"{run['true_n_steps']} steps · gallery_mode=full"
        ),
        "why_broke": why,
        "fairness_notes": spec["fairness_notes"],
        "mean_steps": run["true_n_steps"],
        "true_n_steps_by_seed": {"0": run["true_n_steps"]},
        "seed_factory_ref": spec.get("export") or "",
        "verifier_ref": spec["audit"],
        "canonical_seed": 0,
        "seeds": {},
        "pages": [],
        "provenance": {
            "traj_dir": f"browser-gym-seed-to-cua-gym/trajectories/{spec['traj_dir']}/",
            "audit": spec["audit"],
            "export": spec.get("export") or "",
            "original_mnum": spec["original_mnum"],
            "original_task_id": spec["task_id"],
            "original_slug": spec["slug"],
            "screenshot_dir": f"screens/{episode}/ (FULL gallery)",
            "gcs": spec.get("gcs") or "",
            "execution": spec.get("execution") or "",
            "run_id": spec.get("run_id") or "",
            "notes": (
                "Full step-by-step screenshot gallery (gallery_mode=full). "
                "n_steps == true_n_steps == every PNG the agent took."
            ),
            "gym": str(gym),
            "traj_files": [meta["traj_path"]],
        },
        "requiresSummary": requires,
        "agentDidSummary": agent_did,
    }
    task = {
        "mnum": spec["mnum"],
        "title": spec.get("title") or "",
        "slug": spec["slug"],
        "task_id": spec["task_id"],
        "pool": POOL,
        "prompt": brief,
        "brief_agent": brief,
        "apps": spec["apps"],
        "difficulty": spec["difficulty"],
        "vein": spec["vein"],
        "expected_behaviour": spec["expected_behaviour"],
        "task_design": spec["task_design"] + " Why it broke: " + why,
        "requiresSummary": requires,
        "agentDidSummary": agent_did,
        "has_screenshots": n_png > 0,
        "fairness_notes": spec["fairness_notes"],
        "mean_steps": run["true_n_steps"],
        "true_n_steps_by_seed": {"0": run["true_n_steps"]},
        "gallery_mode": "full",
        "verifier": verifier,
        "env": env,
        "models": [
            {
                "model": "sol",
                "model_full": MODEL,
                "runs": [run],
            }
        ],
        "original_mnum": spec["original_mnum"],
        "original_task_id": spec["task_id"],
        "n_models": 1,
        "n_runs": 1,
        "seed_link": "",
    }
    print(
        f"  {spec['mnum']} seed{run['seed']} {spec['task_id']}: "
        f"{run['true_n_steps']} full steps ({n_png} png) "
        f"score={run['score']} {run['disposition']} ← {episode}"
    )
    return task


def main() -> None:
    gym = find_gym()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tasks = [build_task(spec, gym) for spec in SPECS]
    pkg = {
        "pool": POOL,
        "label": "Breaker-1",
        "short": "Breaker-1",
        "model": MODEL,
        "generated": date.today().isoformat(),
        "notes": (
            "Breaker-1: b1 mp_091 Burrow pickup × GymCal conflict (score 1.0 QuietBreak) + "
            "b2 mp_093 Thursday team lunch cancelled (BREAK gallery score 0.50 — ordered "
            "for May 28 series bait; later HOLD seed0 also exists but is not the review "
            "gallery). Sol seed0 full-trajectory screenshot galleries."
        ),
        "tasks": tasks,
    }
    OUT_PKG.write_text(
        json.dumps(pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"gym: {gym}")
    print(f"wrote {OUT_PKG} ({len(tasks)} tasks)")


if __name__ == "__main__":
    main()
