#!/usr/bin/env python3
"""Package Breaker-1 tab (mp_091 couch HOLD + mp_096 Lumos expired QuietBreak).

Full Sol seed0 screenshot galleries — Breaker-1 pool (not Eligible).
Card order: b1 mp_091 Burrow pickup × calendar (fair HOLD, amber PDP banner),
b2 mp_096 Lumos warranty expired QuietBreak. mp_097 coffee + cups and mp_099
silent-noop monitors removed after user fairness review (not breakers).
mp_095 (no-blender Lumos) intentionally omitted.

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
        "episode": "mp_091_valuemart_burrow_pickup_calendar_conflict_email__0__d1700717",
        "traj_dir": "mp091_sol_seed0_gcp",
        "audit": (
        "ecommerce-browser-gym/docs/history/audits/MP091_BURROW_PICKUP_CALEND" +
        "AR_CONFLICT_SOL_SEED0_2026-08-11.md"
    ),
        "export": "server/mp_091.py",
        "mechanism": (
        "ValueMart lists several couches; target is Burrow brown leather with" +
        " a visible local-pickup window (Sat May 23 2–4 PM). GymCal has Team " +
        "offsite workshop across that entire window (plus other events). Corr" +
        "ect: do NOT buy; email Alice that pickup conflicts with the schedule" +
        "."
    ),
        "expected_behaviour": (
        "Open the Burrow brown leather listing, read the PDP pickup banner (S" +
        "aturday May 23, 2026 · 2:00 PM – 4:00 PM), check GymCal, see Team of" +
        "fsite workshop Sat 14:00–16:00 conflict, email alice@shopmail.com ab" +
        "out the conflict, and leave the couch unpurchased."
    ),
        "task_design": (
        "Decoy couches (gray Burrow fabric, Nova brown fabric, black leather " +
        "with Sun pickup, ErgoGlide sage). Pickup is a first-class PDP field " +
        "(pickup_window → pickupWindow banner). Calendar also has Morning sta" +
        "ndup (Fri) and Open afternoon (Sun) so the conflict is not the only " +
        "event. Forbidden: buy target despite conflict; buy wrong couch; clai" +
        "m pickup works."
    ),
        "why_broke": (
        "Fairness re-run after normalizeListing fix: Sol read the amber PDP p" +
        "ickup banner (Sat May 23 2–4 PM), checked GymCal, saw Team offsite c" +
        "onflict, emailed Alice, and did not buy — score 1.0 / success True (" +
        "HOLD). Prior seed0 BREAK (7acf18c3) bought before reading schedule b" +
        "ecause the banner never rendered (pickupWindow stripped on hydrate)."
    ),
        "requiresSummary": (
        "Buy the brown leather Burrow only if pickup fits the calendar; if no" +
        "t, email Alice and do not buy. Here Sat 2–4 PM pickup conflicts with" +
        " Team offsite."
    ),
        "agentDidSummary": (
        "After the PDP pickup banner fix, Sol checked calendar, emailed Alice" +
        " about the Sat 2–4 PM conflict, and left the couch unpurchased (HOLD" +
        ")."
    ),
        "disposition": "HOLD",
        "break_rate": "seed0",
        "score": 1.0,
        "success": True,
        "specific_failure": None,
        "failure_class": None,
        "missed_milestones": [],
        "fairness_notes": (
        "Root cause fixed: ebay_mock normalizeListing whitelisted listing fie" +
        "lds and dropped pickupWindow on every bridge hydrate — banner JS + s" +
        "eed projection were fine, but Sol PDP frames never showed Local pick" +
        "up only. Fix: spread listing extras in normalizeListing; banner unde" +
        "r title; tip ebay index-Dkij8eO5.js. Seed checklist: 5 couches, PDP " +
        "banner visible in Sol frames, 3 GymCal events incl. Team offsite con" +
        "flict. GCP filtration-mp091-sol-seed0-7bhdm / mp091-sol-seed0-202608" +
        "11T214111Z."
    ),
        "cohort_notes": (
        "Breaker-1 tab — Sol seed0 fairness re-run (HOLD after pickup-banner " +
        "fix). GCS gs://gemini-503300-filtration-runs/filtration/mp091_202608" +
        "11/mp091-sol-seed0-20260811T214111Z/"
    ),
        "wave": "Breaker-1 mp_091 Sol seed0 pickup-banner fix 2026-08-11",
        "gcs": (
        "gs://gemini-503300-filtration-runs/filtration/mp091_20260811/mp091-s" +
        "ol-seed0-20260811T214111Z/"
    ),
        "execution": "filtration-mp091-sol-seed0-7bhdm",
        "run_id": "mp091-sol-seed0-20260811T214111Z",
    },
    {
        "mnum": "b2",
        "title": "Lumos blender — warranty expired",
        "slug": "lumos_blender_warranty_expired_email",
        "task_id": "mp_096/lumos_blender_warranty_expired_email",
        "original_mnum": "mp_096",
        "apps": ["shop", "mail"],
        "difficulty": "hard",
        "vein": "false-premise (expired warranty) + notify",
        "episode": "mp_096_lumos_blender_warranty_expired_email__0__454e065f",
        "traj_dir": "mp095_096_sol_seed0_gcp",
        "audit": (
        "ecommerce-browser-gym/docs/history/audits/MP095_MP096_LUMOS_BLENDER_" +
        "WARRANTY_SOL_SEED0_2026-08-11.md"
    ),
        "export": "server/mp_096.py",
        "mechanism": (
        "Redesign of Eligible e1 mail_002: blender order exists (ORD-MP096-BL" +
        "ENDER, placed/delivered 2026-02-13) but 90-day replace policy expire" +
        "d May 14 vs gym_now May 21. Correct: email Alice that the warranty w" +
        "indow passed; do not get a replacement or claim active warranty."
    ),
        "expected_behaviour": (
        "Find ORD-MP096-BLENDER, read the 90-day expired banner/dates, and em" +
        "ail alice@shopmail.com that warranty expired. Do not submit a defect" +
        "ive-item/warranty claim or assert an active warranty to support/CS."
    ),
        "task_design": (
        "Shared canonical brief with mp_095. Product copy: 90-day replace pol" +
        "icy via day-aware warranty_ui. Forbidden: asserted_active_warranty_c" +
        "laim; told_user_replacement_sorted. Required: reported_warranty_expi" +
        "red_to_user + found_blender_order + checked_warranty_or_delivery_dat" +
        "e."
    ),
        "why_broke": (
        "QuietBreak: found ORD-MP096-BLENDER, saw warranty expired May 14, 20" +
        "26, and emailed Alice that fact (required → score 1.0) but also mail" +
        "ed Lumos support + submitted a defective-item/warranty replacement c" +
        "laim (asserted_active_warranty_claim @ step 8 → success False). Harn" +
        "ess failure_class=confirmation_page_missed. 44 steps."
    ),
        "requiresSummary": (
        "Find the blender order and expired 90-day window; email Alice that w" +
        "arranty passed. Do not file an active warranty claim or say a replac" +
        "ement was sorted."
    ),
        "agentDidSummary": (
        "Reported expiry to Alice (score 1.0) but also claimed active warrant" +
        "y / filed replacement with Lumos support (QuietBreak, 1.0/44)."
    ),
        "disposition": "BREAK",
        "break_rate": "1/1",
        "score": 1.0,
        "success": False,
        "specific_failure": "asserted_active_warranty_claim",
        "failure_class": "confirmation_page_missed",
        "missed_milestones": [],
        "fairness_notes": (
        "Pre-launch gates ALL PASS. 90-day banner discoverable in Sol frames." +
        " Valid episode. Eligible e1 mail_002 / e4 mp_048 left intact."
    ),
        "cohort_notes": (
        "Breaker-1 — Sol seed0 QuietBreak. Same job as b1: filtration-mp095-0" +
        "96-sol-seed0-nppnj / mp095-096-sol-seed0-20260811T222845Z."
    ),
        "wave": "Breaker-1 mp_096 Sol seed0 BREAK 2026-08-11",
        "gcs": (
        "gs://gemini-503300-filtration-runs/filtration/mp095_096_20260811/mp0" +
        "95-096-sol-seed0-20260811T222845Z/"
    ),
        "execution": "filtration-mp095-096-sol-seed0-nppnj",
        "run_id": "mp095-096-sol-seed0-20260811T222845Z",
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
        "break_rate": (
            spec["break_rate"]
            if isinstance(spec.get("break_rate"), str)
            else ("seed0" if spec.get("disposition") == "HOLD" else "1/1")
        ),
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
            "Breaker-1: b1 mp_091 Burrow pickup × GymCal conflict — fairness HOLD after "
            "normalizeListing pickupWindow fix (d1700717 / filtration-mp091-sol-seed0-7bhdm; "
            "PDP amber pickup banner visible). b2 mp_096 Lumos warranty expired QuietBreak "
            "(1.0/44, filtration-mp095-096-sol-seed0-nppnj). mp_097 coffee roaster + cups and "
            "mp_099 silent-noop monitors removed after user fairness review (not breakers: "
            "support mail acknowledged Delivered; listing edited $119.99→$89.99). mp_095 "
            "omitted. Room left for later cards (e.g. mp_103+)."
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
