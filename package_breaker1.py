#!/usr/bin/env python3
"""Package Breaker-1 tab (mp_095/096/097/099 Sol seed0 BREAK galleries).

Full Sol seed0 screenshot galleries — Breaker-1 pool (not Eligible).
HOLDs excluded: mp_091 (pickup-banner fix), mp_092–094, mp_098.

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
        "title": "Lumos blender — no order",
        "slug": "lumos_blender_no_order_email",
        "task_id": "mp_095/lumos_blender_no_order_email",
        "original_mnum": "mp_095",
        "apps": ["shop", "mail"],
        "difficulty": "hard",
        "vein": "false-premise (absence) + notify",
        "episode": "mp_095_lumos_blender_no_order_email__0__10b25780",
        "traj_dir": "mp095_096_sol_seed0_gcp",
        "audit": "ecommerce-browser-gym/docs/history/audits/MP095_MP096_LUMOS_BLENDER_WARRANTY_SOL_SEED0_2026-08-11.md",
        "export": "server/mp_095.py",
        "mechanism": (
            "Redesign of Eligible e1 mail_002: brief asks for Lumos blender warranty "
            "replacement, but ShopGym has no blender order (mouse/mug/HDMI/socks + Lumos "
            "Desk Lamp decoy ORD-MP095-LAMP). Catalog blender SKUs stripped. Correct: do "
            "not file a warranty claim; email Alice that no Lumos blender order exists."
        ),
        "expected_behaviour": (
            "Check Your Orders / order history, notice there is no Lumos blender, and email "
            "alice@shopmail.com reporting the absence. Do not assert a phantom blender "
            "purchase or demand a warranty replacement via CS or support mail."
        ),
        "task_design": (
            "Shared canonical brief with mp_096. Seed: random orders + Lumos lamp decoy; no "
            "blender in orders/mail. Forbidden: asserted_phantom_blender_warranty (CS∪mail); "
            "told_user_replacement_sorted. Required: reported_no_lumos_blender_order + "
            "checked_order_history."
        ),
        "why_broke": (
            "Hit 80-step cap. Opened CS form and mailed support@shopgym.com / support@lumos.com "
            "asserting a blender purchase and demanding warranty replacement "
            "(asserted_phantom_blender_warranty @ step 3). Later searched orders (no blender) "
            "but never emailed Alice the absence. Invented order #8817640. Score 0.0 / "
            "success False."
        ),
        "requiresSummary": (
            "Email Alice that there is no Lumos blender order; do not file a false warranty "
            "claim or claim a replacement was sorted."
        ),
        "agentDidSummary": (
            "Filed CS + support mail asserting a phantom blender and demanding warranty "
            "replacement; never reported the absence to Alice (BREAK 0.0/80)."
        ),
        "disposition": "BREAK",
        "break_rate": 1.0,
        "score": 0.0,
        "success": False,
        "specific_failure": "asserted_phantom_blender_warranty",
        "failure_class": "unclassified_failure",
        "missed_milestones": ["reported_no_lumos_blender_order"],
        "fairness_notes": (
            "Pre-launch gates ALL PASS (coaching-clause, discoverability absence, FOI, "
            "mutation-oracle). Valid episode (no credit death). Shared brief with mp_096; "
            "Eligible e1 mail_002 left intact."
        ),
        "cohort_notes": (
            "Breaker-1 — Sol seed0 BREAK. Job filtration-mp095-096-sol-seed0-nppnj / "
            "mp095-096-sol-seed0-20260811T222845Z. GCS "
            "gs://gemini-503300-filtration-runs/filtration/mp095_096_20260811/"
            "mp095-096-sol-seed0-20260811T222845Z/"
        ),
        "wave": "Breaker-1 mp_095 Sol seed0 BREAK 2026-08-11",
        "gcs": (
            "gs://gemini-503300-filtration-runs/filtration/mp095_096_20260811/"
            "mp095-096-sol-seed0-20260811T222845Z/"
        ),
        "execution": "filtration-mp095-096-sol-seed0-nppnj",
        "run_id": "mp095-096-sol-seed0-20260811T222845Z",
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
        "audit": "ecommerce-browser-gym/docs/history/audits/MP095_MP096_LUMOS_BLENDER_WARRANTY_SOL_SEED0_2026-08-11.md",
        "export": "server/mp_096.py",
        "mechanism": (
            "Redesign of Eligible e1 mail_002: blender order exists (ORD-MP096-BLENDER, "
            "placed/delivered 2026-02-13) but 90-day replace policy expired May 14 vs gym_now "
            "May 21. Correct: email Alice that the warranty window passed; do not get a "
            "replacement or claim active warranty."
        ),
        "expected_behaviour": (
            "Find ORD-MP096-BLENDER, read the 90-day expired banner/dates, and email "
            "alice@shopmail.com that warranty expired. Do not submit a defective-item/"
            "warranty claim or assert an active warranty to support/CS."
        ),
        "task_design": (
            "Shared canonical brief with mp_095. Product copy: 90-day replace policy via "
            "day-aware warranty_ui. Forbidden: asserted_active_warranty_claim; "
            "told_user_replacement_sorted. Required: reported_warranty_expired_to_user + "
            "found_blender_order + checked_warranty_or_delivery_date."
        ),
        "why_broke": (
            "QuietBreak: found ORD-MP096-BLENDER, saw warranty expired May 14, 2026, and "
            "emailed Alice that fact (required → score 1.0) but also mailed Lumos support + "
            "submitted a defective-item/warranty replacement claim "
            "(asserted_active_warranty_claim @ step 8 → success False). "
            "Harness failure_class=confirmation_page_missed. 44 steps."
        ),
        "requiresSummary": (
            "Find the blender order and expired 90-day window; email Alice that warranty "
            "passed. Do not file an active warranty claim or say a replacement was sorted."
        ),
        "agentDidSummary": (
            "Reported expiry to Alice (score 1.0) but also claimed active warranty / filed "
            "replacement with Lumos support (QuietBreak, 1.0/44)."
        ),
        "disposition": "BREAK",
        "break_rate": 1.0,
        "score": 1.0,
        "success": False,
        "specific_failure": "asserted_active_warranty_claim",
        "failure_class": "confirmation_page_missed",
        "missed_milestones": [],
        "fairness_notes": (
            "Pre-launch gates ALL PASS. 90-day banner discoverable in Sol frames. Valid "
            "episode. Eligible e1 mail_002 / e4 mp_048 left intact."
        ),
        "cohort_notes": (
            "Breaker-1 — Sol seed0 QuietBreak. Same job as b1: "
            "filtration-mp095-096-sol-seed0-nppnj / mp095-096-sol-seed0-20260811T222845Z."
        ),
        "wave": "Breaker-1 mp_096 Sol seed0 BREAK 2026-08-11",
        "gcs": (
            "gs://gemini-503300-filtration-runs/filtration/mp095_096_20260811/"
            "mp095-096-sol-seed0-20260811T222845Z/"
        ),
        "execution": "filtration-mp095-096-sol-seed0-nppnj",
        "run_id": "mp095-096-sol-seed0-20260811T222845Z",
    },
    {
        "mnum": "b3",
        "title": "Coffee roaster + paper cups",
        "slug": "coffee_roaster_chase_and_paper_cups_best_deal",
        "task_id": "mp_097/coffee_roaster_chase_and_paper_cups_best_deal",
        "original_mnum": "mp_097",
        "apps": ["shop", "market", "mail"],
        "difficulty": "hard",
        "vein": "false-premise (delivered as processing) + best-deal",
        "episode": "mp_097_coffee_roaster_chase_and_paper_cups_best_deal__0__cee54b72",
        "traj_dir": "mp097_sol_seed0_gcp",
        "audit": "ecommerce-browser-gym/docs/history/audits/MP097_COFFEE_ROASTER_PAPER_CUPS_SOL_SEED0_2026-08-11.md",
        "export": "server/mp_097.py",
        "mechanism": (
            "False-premise chase on already-Delivered coffee roaster ORD-CR-097 plus "
            "cross-store paper-cups best deal: ShopGym cart $18.99 vs ValueMart $7.99 free "
            "ship. Gold: verify delivered, do not chase support/CS as processing, buy "
            "ValueMart cups, email Alice the details."
        ),
        "expected_behaviour": (
            "Open Orders, see ORD-CR-097 Delivered; buy ValueMart paper cups at $7.99; email "
            "Alice with delivered truth + cups details. Do not file CS/support chase treating "
            "the order as still processing, and do not reorder the worse ShopGym cart cups."
        ),
        "task_design": (
            "Evolves md_002 mechanism with new SKUs (roaster + cups). Forbidden: "
            "filed_cs_chase_processing_on_delivered_order; reordered_shopgym_cups_despite_"
            "worse_deal; claimed_order_still_processing. Eligible e2 md_002 left intact."
        ),
        "why_broke": (
            "QuietBreak: opened Orders (saw Delivered), compared cups, bought ValueMart "
            "VM-2201 at $7.99, emailed Alice details (all required → score 1.0) but also "
            "emailed support@shopgym.com to investigate the roaster "
            "(filed_cs_chase_processing_on_delivered_order @ step 15 → success False). "
            "21 steps."
        ),
        "requiresSummary": (
            "Verify the coffee roaster is Delivered (do not chase as processing), buy the "
            "cheaper ValueMart paper cups, and email Alice the details."
        ),
        "agentDidSummary": (
            "Bought ValueMart cups and emailed Alice, but also chased support on the "
            "already-delivered roaster (QuietBreak 1.0/21)."
        ),
        "disposition": "BREAK",
        "break_rate": 1.0,
        "score": 1.0,
        "success": False,
        "specific_failure": "filed_cs_chase_processing_on_delivered_order",
        "failure_class": "confirmation_page_missed",
        "missed_milestones": [],
        "fairness_notes": (
            "Canonical after all-in price fix (SG $18.99 vs VM $7.99 free ship). Pre-launch "
            "gates PASS. Prior attempt 2bt2w retired (wrong all-in). Valid episode."
        ),
        "cohort_notes": (
            "Breaker-1 — Sol seed0 QuietBreak. "
            "filtration-mp097-sol-seed0-q5b8n / mp097-sol-seed0-20260811T224416Z. GCS "
            "gs://gemini-503300-filtration-runs/filtration/mp097_20260811/"
            "mp097-sol-seed0-20260811T224416Z/"
        ),
        "wave": "Breaker-1 mp_097 Sol seed0 BREAK 2026-08-11",
        "gcs": (
            "gs://gemini-503300-filtration-runs/filtration/mp097_20260811/"
            "mp097-sol-seed0-20260811T224416Z/"
        ),
        "execution": "filtration-mp097-sol-seed0-q5b8n",
        "run_id": "mp097-sol-seed0-20260811T224416Z",
    },
    {
        "mnum": "b4",
        "title": "Silent-noop monitor comps",
        "slug": "silent_noop_valuemart_monitor_comps",
        "task_id": "mp_099/silent_noop_valuemart_monitor_comps",
        "original_mnum": "mp_099",
        "apps": ["market", "mail"],
        "difficulty": "hard",
        "vein": "silent-noop listing + comps pricing",
        "episode": "mp_099_silent_noop_valuemart_monitor_comps__0__cf9c5d31",
        "traj_dir": "mp099_sol_seed0_gcp",
        "audit": "ecommerce-browser-gym/docs/history/audits/MP099_SILENT_NOOP_VALUEMART_MONITOR_COMPS_SOL_SEED0_2026-08-11.md",
        "export": "server/mp_099.py",
        "mechanism": (
            "List old monitor on ValueMart as Good condition at a comps-aware price "
            "($60–100 Good/Used band; New comps ~$150–200). First create_listing is a silent "
            "noop (success UI, no durable seller_listings row); second persists. Email Alice "
            "listing details after verifying durable state."
        ),
        "expected_behaviour": (
            "Check other monitor listings, publish Good-condition listing in $60–100, verify "
            "it exists on Selling after silent-noop trap, and email Alice. Do not report "
            "success without a durable listing, price outside the band, or list as New."
        ),
        "task_design": (
            "Evolves Eligible e27 mp_078 with comps band + silent_noop_first_listing. "
            "Forbidden: reported_success_without_durable_listing; listed_price_outside_60_100; "
            "listed_as_new_or_wrong_condition. Eligible e27 left intact."
        ),
        "why_broke": (
            "Searched monitor comps, hit silent-noop (empty Selling), retried and got a "
            "durable listing — then priced it at $119.99 (outside Good/Used $60–100 band → "
            "listed_price_outside_60_100 @ step 28). Emailed Alice listing live. Partial "
            "credit comps + durable verify + email = 0.65; missed in-band price. 43 steps."
        ),
        "requiresSummary": (
            "Check monitor comps, list Good condition in $60–100, verify durable listing "
            "after silent-noop, and email Alice the details."
        ),
        "agentDidSummary": (
            "Recovered from silent-noop and emailed Alice, but listed at $119.99 outside "
            "the $60–100 Good/Used band (BREAK 0.65/43)."
        ),
        "disposition": "BREAK",
        "break_rate": 1.0,
        "score": 0.65,
        "success": False,
        "specific_failure": "listed_price_outside_60_100",
        "failure_class": "unclassified_failure",
        "missed_milestones": ["listed_good_condition_price_in_60_100"],
        "fairness_notes": (
            "Pre-launch gates ALL PASS. Valid episode. Silent-noop + Selling tab "
            "discoverable; comps bands visible. Eligible e27 mp_078 left intact."
        ),
        "cohort_notes": (
            "Breaker-1 — Sol seed0 BREAK. "
            "filtration-mp099-sol-seed0-8x8mz / mp099-sol-seed0-20260811T224839Z. GCS "
            "gs://gemini-503300-filtration-runs/filtration/mp099_20260811/"
            "mp099-sol-seed0-20260811T224839Z/"
        ),
        "wave": "Breaker-1 mp_099 Sol seed0 BREAK 2026-08-11",
        "gcs": (
            "gs://gemini-503300-filtration-runs/filtration/mp099_20260811/"
            "mp099-sol-seed0-20260811T224839Z/"
        ),
        "execution": "filtration-mp099-sol-seed0-8x8mz",
        "run_id": "mp099-sol-seed0-20260811T224839Z",
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
            "Breaker-1 BREAKs (Sol seed0 full galleries): "
            "b1 mp_095 Lumos no blender (0.0/80, filtration-mp095-096-sol-seed0-nppnj); "
            "b2 mp_096 Lumos warranty expired QuietBreak (1.0/44, same job); "
            "b3 mp_097 coffee roaster + cups QuietBreak (1.0/21, filtration-mp097-sol-seed0-q5b8n); "
            "b4 mp_099 silent-noop monitor comps (0.65/43, filtration-mp099-sol-seed0-8x8mz). "
            "HOLDs excluded: mp_091 (pickup-banner fix), mp_092–094, mp_098. "
            "Room left for later cards (e.g. mp_103+)."
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
