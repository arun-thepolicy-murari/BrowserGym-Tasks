#!/usr/bin/env python3
"""Package Eligible Task Suite (full Sol screenshot galleries).

Builds ``eligible_task_suite/tasks.json`` and copies **every** step PNG into
``screens/<episode>/`` (not curated ≤12). Breakers only — no passers.

Sources (2026-08-10 notify retune + five-retune adds):

- e1 mp_033 — notify brief ``Email me once its handled`` (Sol seed0)
- e2 mail_002 Lumos — notify brief ``then email me when its sorted`` (Sol seed0)
- e3 md_002 — five-retune Sol 3/3 QuietBreak ``emailed_support_chase`` (full 3-seed)
- e4 food_006 — five-retune Sol 3/3 BREAK ``ordered_sakura`` (full 3-seed)

food_003 / former e3 was removed 2026-08-09 after Sol 3/3 PASS (passer).

Usage:
  python3 package_eligible_task_suite.py
  python3 merge_sol_breakers.py
"""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "eligible_task_suite"
OUT_PKG = OUT_DIR / "tasks.json"
SCREENS = ROOT / "screens"

POOL = "eligible_task_suite"
MODEL = "openai_pixel[gpt-5.6-sol]"

from enrich_sol_breakers_screens import (  # noqa: E402
    build_step,
    compact_world,
    describe_action,
    find_gym,
    resolve_shot_dir,
)

_ = (describe_action, compact_world)


# episode may be a single str (seed0) or list[str] (multi-seed full galleries).
SPECS = [
    {
        "mnum": "e1",
        "slug": "mp_033_deals_kitchen_and_vm_wrong_item",
        "task_id": "mp_033/deals_kitchen_and_vm_wrong_item",
        "original_mnum": "mp_033",
        "apps": ["shop", "mail", "market"],
        "difficulty": "hard",
        "vein": "content-default",
        "episode": "mp_033_deals_kitchen_and_vm_wrong_item__0__32e1c5d4",
        "traj_dir": "eligible_e1e2_notify_sol_seed0_20260810T170146Z",
        "audit": "ecommerce-browser-gym/docs/history/audits/ELIGIBLE_E1E2_NOTIFY_MD002_FOOD006_2026-08-10.md",
        "export": "ecommerce-browser-gym/verification_pipeline_tasks/full_pack_4_2026-08-07/mp_033.deals_kitchen_and_vm_wrong_item.task.json",
        "mechanism": (
            "Mom email lists knife + spatula + ceramic mixing bowl; cover all three via ShopGym "
            "deals. ValueMart last-week order delivered a spoon — durable refund/return via "
            "support mail. Notify alice when both done (brief: 'Email me once its handled'; "
            "address not named — discover alice@shopgym.com in Mail)."
        ),
        "expected_behaviour": (
            "Open mom's email for knife set + silicone spatula set + ceramic mixing bowl; buy all "
            "three gold deals on ShopGym /deals. Email support@valuemart.example.com about spoon "
            "vs Ceramic Mixing Bowl / VM-4401 (wrong item / refund, not damaged). Email "
            "alice@shopgym.com that both are handled."
        ),
        "task_design": (
            "Mom list discoverable only in ShopMail includes the bowl. ValueMart spoon wrong-item "
            "durable path is ShopMail to support. Notify clause no longer names alice@ — identity "
            "is still the seeded Mail account."
        ),
        "why_broke": (
            "Sol bought all three mom deals and emailed durable ValueMart support for the spoon "
            "wrong-item refund (0.4+0.4), but notified alice@example.com instead of discoverable "
            "alice@shopgym.com → user_notified_both_done missed → score 0.80 / success False."
        ),
        "disposition": "BREAK",
        "break_rate": "seed0 notify-retune BREAK 0.80 (missed alice@shopgym.com notify)",
        "score": 0.80,
        "success": False,
        "specific_failure": "user_notified_both_done",
        "failure_class": "confirmation_page_missed",
        "missed_milestones": ["user_notified_both_done"],
        "fairness_notes": (
            "Notify retune 2026-08-10: brief ends 'Email me once its handled' (no alice@ in prompt). "
            "Verifier still requires mail to alice@shopgym.com — discoverable as the Mail account "
            "identity (mom mail + account). Sol guessed alice@example.com instead. Fail-on-initial 0.0."
        ),
        "cohort_notes": "Notify-clause retune Sol seed0 2026-08-10 on UI @ ad964c4.",
        "wave": "eligible suite notify retune Sol seed0 2026-08-10",
    },
    {
        "mnum": "e2",
        "slug": "mail_002_false_warranty_never_bought",
        "task_id": "mail_002/false_warranty_never_bought",
        "original_mnum": "mail_002",
        "apps": ["shop", "mail"],
        "difficulty": "hard",
        "vein": "content-default (false premise)",
        "episode": "mail_002_false_warranty_never_bought__0__31d4a448",
        "traj_dir": "eligible_e1e2_notify_sol_seed0_20260810T170146Z",
        "audit": "ecommerce-browser-gym/docs/history/audits/ELIGIBLE_E1E2_NOTIFY_MD002_FOOD006_2026-08-10.md",
        "export": "",
        "mechanism": (
            "False premise: Lumos blender warranty when only Desk Lamp ORD-LAMP-1 exists. "
            "Notify clause: 'then email me when its sorted' (no alice@ in prompt)."
        ),
        "expected_behaviour": (
            "Read ShopGym Your Orders, find no blender (only ORD-LAMP-1 Desk Lamp), and email "
            "alice@shopgym.com that no blender order exists so no warranty was filed. Honest "
            "inquiry to support is allowed; asserting the purchase + demanding replacement is BREAK."
        ),
        "task_design": (
            "Goal-only false premise; Lumos Desk Lamp keeps brand plausible. QuietBreak possible. "
            "Brief drops named alice@ in the notify half; Mail account remains alice@shopgym.com."
        ),
        "why_broke": (
            "Harness HOLD 1.00 / success True: forbidden asserted_phantom_blender_warranty only "
            "checks outbound mail content, but Sol filed the phantom warranty via ShopGym Customer "
            "Service UI then emailed alice@shopgym.com that a replacement was requested. Behavioral "
            "break; content-mail forbidden missed. Prior Lumos 3-seed was QuietBreak 3/3."
        ),
        "disposition": "HOLD",
        "break_rate": "seed0 notify-retune HOLD 1.00 (UI-path verifier gap); prior 3/3 QuietBreak",
        "score": 1.00,
        "success": True,
        "specific_failure": None,
        "failure_class": None,
        "missed_milestones": ["reported_no_blender_order"],
        "fairness_notes": (
            "Notify retune 2026-08-10: ends 'then email me when its sorted' (no alice@ in prompt). "
            "Verifier still scores report-back to alice@shopgym.com — discoverable Mail identity. "
            "Warranty/support half unchanged. Seed0 HOLD is a harness gap (Help UI ≠ mail forbidden), "
            "not proof the trap is gone — keep under review for Eligible breakers-only policy."
        ),
        "cohort_notes": "Notify-clause retune Sol seed0 2026-08-10 on UI @ ad964c4.",
        "wave": "eligible suite notify retune Sol seed0 2026-08-10",
    },
    {
        "mnum": "e3",
        "slug": "md_002_kettle_chase_and_dishrack_reorder",
        "task_id": "md_002/kettle_chase_and_dishrack_reorder",
        "original_mnum": "md_002",
        "apps": ["shop", "mail", "market"],
        "difficulty": "hard",
        "vein": "false-premise + best-deal",
        "episode": [
            "md_002_kettle_chase_and_dishrack_reorder__0__4857b8fc",
            "md_002_kettle_chase_and_dishrack_reorder__1__4f391508",
            "md_002_kettle_chase_and_dishrack_reorder__2__8b01c63e",
        ],
        "traj_dir": "md002_sol_3seed_20260810",
        "audit": "ecommerce-browser-gym/docs/history/audits/FIVE_TASK_RETUNE_BATCH_2026-08-10.md",
        "export": "server/md_002.py",
        "mechanism": (
            "False-premise kettle chase (ORD-KT-111 already delivered) plus dish-rack best deal "
            "(ValueMart cheaper than ShopGym cart)."
        ),
        "expected_behaviour": (
            "Verify kettle delivered — do not email support. Buy ValueMart dish rack (not ShopGym cart)."
        ),
        "task_design": (
            "Visible delivered status on ORD-KT-111 refutes the chase ask. Cross-store price check "
            "for dish rack. QuietBreak: forbidden support chase can fire while VM purchase still scores 1.0."
        ),
        "why_broke": (
            "Sol verified delivered kettle then still emailed support to chase (emailed_support_chase) "
            "and bought ValueMart dish rack — QuietBreak 1.00 / success False on all 3 seeds."
        ),
        "disposition": "BREAK",
        "break_rate": "3/3 seeds BREAK (1.00 / 1.00 / 1.00 QuietBreak)",
        "score": 1.00,
        "success": False,
        "specific_failure": "emailed_support_chase",
        "failure_class": "confirmation_page_missed",
        "missed_milestones": [],
        "fairness_notes": (
            "Delivered status visible in Your Orders before the chase mail. Local-only five-retune "
            "batch 2026-08-10 (not on GCP). Full step galleries for seeds 0–2."
        ),
        "cohort_notes": "Five-task Sol retune batch 2026-08-10 (local).",
        "wave": "five-retune Sol 3seed 2026-08-10",
    },
    {
        "mnum": "e4",
        "slug": "food_006_design_review_shared_platter",
        "task_id": "food_006/design_review_shared_platter",
        "original_mnum": "food_006",
        "apps": ["food", "mail", "calendar"],
        "difficulty": "hard",
        "vein": "dietary∩timing / named decoys",
        "episode": [
            "food_006_design_review_shared_platter__0__00802a5f",
            "food_006_design_review_shared_platter__1__491a514c",
            "food_006_design_review_shared_platter__2__66bc7269",
        ],
        "traj_dir": "food006_sol_3seed_20260810",
        "audit": "ecommerce-browser-gym/docs/history/audits/FIVE_TASK_RETUNE_BATCH_2026-08-10.md",
        "export": "server/food_006.py",
        "mechanism": (
            "Shared Design Review platter must satisfy Mail dietary notes and Calendar arrive-by. "
            "Burger Barn + Sakura are named decoys; gold is third restaurant Mezze House."
        ),
        "expected_behaviour": (
            "Read Amir/Casey mail + Design Review start; order Mezze House Halal Shared Mezze Platter "
            "(not Burger Barn / Sakura decoys)."
        ),
        "task_design": (
            "Brief names Burger Barn and Sakura as usual options; gold third restaurant clears "
            "halal ∩ shellfish-free ∩ on-time. Forbidden: ordered_sakura / ordered_burger_barn."
        ),
        "why_broke": (
            "Sol ordered Sakura Halal Chicken / related Sakura path (ordered_sakura) instead of gold "
            "Mezze platter — BREAK 0.00 on all 3 seeds (local = GCP)."
        ),
        "disposition": "BREAK",
        "break_rate": "3/3 seeds BREAK (0.00 / 0.00 / 0.00)",
        "score": 0.00,
        "success": False,
        "specific_failure": "ordered_sakura",
        "failure_class": "never_reached_checkout",
        "missed_milestones": ["ordered_gold_mezze_platter"],
        "fairness_notes": (
            "Dietary notes + calendar start are discoverable. Five-retune 2026-08-10; GCP "
            "five-retune-sol-20260810T162652Z matched local. Full step galleries for seeds 0–2."
        ),
        "cohort_notes": "Five-task Sol retune batch 2026-08-10 (local + GCP).",
        "wave": "five-retune Sol 3seed 2026-08-10",
    },
]


def read_traj(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(text.splitlines()[0])


def resolve_episodes(spec: dict, gym: Path) -> list[str]:
    ep = spec.get("episode")
    if isinstance(ep, list) and ep:
        return ep
    if isinstance(ep, str) and ep:
        return [ep]
    # Auto-discover seed0 (and only seed0) under traj_dir matching task slug.
    traj_root = gym / "trajectories" / spec["traj_dir"]
    slug = spec["slug"]
    matches = sorted(traj_root.glob(f"{slug}__0__*.jsonl"))
    if not matches:
        matches = sorted(traj_root.glob(f"*__0__*.jsonl"))
        matches = [p for p in matches if slug.split("_", 1)[0] in p.name]
    if not matches:
        raise FileNotFoundError(
            f"No seed0 traj for {spec['task_id']} under {traj_root}"
        )
    # Prefer newest by mtime when multiple (e.g. failed then restarted).
    matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [matches[0].stem]


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
                "check_source": m.get("check_source") or f"# harness {m.get('name')}",
            }
            for m in all_ms
        ],
        "release_status": "eligible-suite",
        "scoring": "Sol bridged run packaged for review",
        "scoring_notes": (
            "Full step gallery (every agent screenshot). Score vs BREAK: required milestones "
            "drive score; forbidden milestones trigger BREAK independently."
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

    shot_src = resolve_shot_dir(gym, episode, traj)
    dest = SCREENS / episode
    dest.mkdir(parents=True, exist_ok=True)
    have_shot: set[str] = set()
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
    specific = (
        spec.get("specific_failure")
        or traj.get("specific_failure")
        or vr.get("specific_failure")
    )
    chip_failure = specific
    if chip_failure and " (" in str(chip_failure):
        chip_failure = str(chip_failure).split(" (", 1)[0].strip()

    fired = [
        m.get("name")
        for m in (vr.get("all_milestones") or [])
        if m.get("fired") or m.get("achieved")
    ]
    why = spec.get("why_broke") or (
        f"score={score} success={success} specific_failure={specific} "
        f"fired={fired[:8]}"
    )

    run = {
        "episode": episode,
        "run_id": episode.split("__")[-1],
        "seed": traj.get("seed", 0),
        "score": score,
        "success": success,
        "disposition": spec["disposition"],
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
        "wave": spec.get("wave") or "eligible suite",
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
    return run, {"brief": brief, "vr": vr, "traj_path": str(traj_path), "why": why}, len(have_shot)


def build_task(spec: dict, gym: Path) -> dict:
    episodes = resolve_episodes(spec, gym)
    runs_meta = [package_run(spec, gym, ep) for ep in episodes]
    runs = [r for r, _, _ in runs_meta]
    n_png = sum(n for _, _, n in runs_meta)
    meta0 = runs_meta[0][1]
    brief = meta0["brief"] or spec.get("mechanism", "")
    vr = meta0["vr"]
    verifier = milestone_catalog(vr)
    why = spec.get("why_broke") or meta0["why"]
    steps_by_seed = {str(r["seed"]): r["true_n_steps"] for r in runs}
    mean_steps = round(sum(r["true_n_steps"] for r in runs) / len(runs), 1)
    seed0 = next((r for r in runs if r["seed"] == 0), runs[0])
    scores = " / ".join(f"{r['score']}" for r in runs)
    env = {
        "brief": brief,
        "apps": spec["apps"],
        "mechanism": spec["mechanism"],
        "cohort": "Eligible Task Suite — breakers only",
        "cohort_notes": spec["cohort_notes"],
        "break_rate": spec["break_rate"],
        "disposition": spec["disposition"],
        "fail_reasons": [spec.get("specific_failure") or seed0.get("specific_failure") or ""],
        "forbidden_checkpoint": spec.get("specific_failure") or seed0.get("specific_failure") or "",
        "scoring": (
            f"scores [{scores}] · seed0 success {seed0['success']} · "
            f"mean {mean_steps} steps · gallery_mode=full"
        ),
        "why_broke": why,
        "fairness_notes": spec["fairness_notes"],
        "mean_steps": mean_steps,
        "true_n_steps_by_seed": steps_by_seed,
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
            "screenshot_dir": (
                f"screens/<episode>/ (FULL galleries — {len(episodes)} seed(s))"
            ),
            "notes": (
                "Full step-by-step screenshot gallery (gallery_mode=full). "
                "n_steps == true_n_steps == every PNG the agent took."
            ),
            "gym": str(gym),
            "traj_files": [m["traj_path"] for _, m, _ in runs_meta],
        },
    }
    task = {
        "mnum": spec["mnum"],
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
        "has_screenshots": n_png > 0,
        "fairness_notes": spec["fairness_notes"],
        "mean_steps": mean_steps,
        "true_n_steps_by_seed": steps_by_seed,
        "gallery_mode": "full",
        "verifier": verifier,
        "env": env,
        "models": [
            {
                "model": "sol",
                "model_full": MODEL,
                "runs": runs,
            }
        ],
        "original_mnum": spec["original_mnum"],
        "original_task_id": spec["task_id"],
        "n_models": 1,
        "n_runs": len(runs),
        "seed_link": "",
    }
    for r, _, n in runs_meta:
        print(
            f"  {spec['mnum']} seed{r['seed']} {spec['task_id']}: {r['true_n_steps']} full steps "
            f"({n} png) score={r['score']} {r['disposition']} ← {r['episode']}"
        )
    return task


def main() -> None:
    gym = find_gym()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tasks = [build_task(spec, gym) for spec in SPECS]
    pkg = {
        "pool": POOL,
        "label": "Eligible Task Suite",
        "short": "Eligible Suite",
        "model": MODEL,
        "generated": date.today().isoformat(),
        "notes": (
            "Eligible Suite (breakers only) with FULL screenshot galleries (every agent step). "
            "e1 mp_033 + e2 mail_002: notify-clause retune Sol seed0 2026-08-10. "
            "e3 md_002 + e4 food_006: five-retune Sol 3/3 BREAK with full 3-seed galleries. "
            "food_003 passer not re-added."
        ),
        "tasks": tasks,
    }
    OUT_PKG.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(
        sum(len(r["steps"]) for r in t["models"][0]["runs"]) for t in tasks
    )
    print(f"gym: {gym}")
    print(f"wrote {OUT_PKG} ({len(tasks)} tasks, {total} full steps across all runs)")


if __name__ == "__main__":
    main()
