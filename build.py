#!/usr/bin/env python3
"""Build the Phase 2 annotation platform.

Merges two sources for the 14 bridged-pilot wave-1 tasks:

  1. Phase 1 platform (``Traj Annotation Tool/data.json`` + ``screens/``) — one run
     per model for models such as oracle / opus 4.8 / gpt 5.6 / sonnet 4.6 / qwen 235b.
  2. ``new_samples/`` — the authoritative gpt-5.5 bridged pilot package, three seeds
     per task, with full trajectories, seed factory payloads and verifier source.

Outputs ``data.json``, a self-contained ``index.html`` and the ``screens/`` folder.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHASE1 = ROOT.parent / "Traj Annotation Tool"
SAMPLES = ROOT / "new_samples"
SCREENS = ROOT / "screens"
TASK_ENV = ROOT / "task_env"
APP = ROOT / "app"

# The 14 tasks in the wave-1 package, in the order the handoff README lists them.
TASK_ORDER = [
    "M73", "M75", "M77", "M78", "M82", "M83", "M84",
    "M87", "M95", "M96", "M97", "M99", "M100", "M111",
]

NEW_WAVE = "bridged pilot w1"
LEGACY_WAVE = "phase 1"

# Phase 1 contributed one older run per model (oracle / opus 4.8 / gpt 5.6 / gpt 5.1 /
# sonnet 4.6 / qwen 235b). Those are retired: only the current wave-1 runs are annotated.
# Phase 1 is still read for task metadata (prompt, trap, verifier, expected behaviour).
# Set this back to True to restore the cross-model runs — no source data was deleted.
INCLUDE_PHASE1_RUNS = False

# Model tabs are ordered so the model under test comes first and the gold path last.
MODEL_ORDER = ["gpt 5.5", "gpt 5.6", "gpt 5.1", "opus 4.8", "sonnet 4.6", "qwen 235b", "oracle"]


def die(msg: str) -> None:
    sys.exit(f"build: {msg}")


def normalise_model(agent_name: str) -> str:
    """``openai_pixel[gpt-5.5]`` -> ``gpt 5.5`` (the label Phase 1 uses)."""
    m = re.search(r"\[([^\]]+)\]", agent_name or "")
    raw = m.group(1) if m else (agent_name or "unknown")
    return raw.replace("-", " ").strip()


def describe_action(kind: str, args: dict) -> str:
    """Render an action the same way Phase 1 renders it, so both waves read alike."""
    args = args or {}
    if kind == "click_mark":
        return f"click_mark {args.get('role','')} \u201c{args.get('name','')}\u201d".strip()
    if kind == "type_into_mark":
        parts = [f"mark_id={args.get('mark_id')}", f"value={args.get('value','')}"]
        if args.get("role"):
            parts.append(f"role={args['role']}")
        if args.get("name"):
            parts.append(f"name={args['name']}")
        return "type_into_mark " + ", ".join(parts)
    if not args:
        return f"{kind} "
    return f"{kind} " + ", ".join(f"{k}={v}" for k, v in args.items() if k != "coord")


def compact_world(world: dict) -> dict:
    """Keep the evidence annotators need (cart, orders, log) and drop the bulk.

    A full ``world_after`` is ~11 KB per step; the catalogue and user profile repeat
    unchanged on every step, so only the mutating slices are carried into data.json.
    """
    if not isinstance(world, dict):
        return {}
    shop = world.get("shop") or {}
    out = {}
    for key in ("cart", "orders", "returns", "subscriptions"):
        val = shop.get(key)
        if val:
            out[key] = val
    if shop.get("action_log"):
        out["action_log"] = shop["action_log"][-12:]
    if shop.get("flash_messages"):
        out["flash_messages"] = shop["flash_messages"]
    for app_name in ("mail", "food", "calendar", "market", "events", "schedule"):
        app_state = world.get(app_name)
        if isinstance(app_state, dict):
            trimmed = {
                k: v for k, v in app_state.items()
                if v not in (None, "", [], {}, 0, False)
                and k not in ("task_id", "seed", "step", "finished")
            }
            if trimmed:
                out[app_name] = trimmed
    return out


def read_json(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


# --------------------------------------------------------------------------- #
# screenshots
# --------------------------------------------------------------------------- #

def copy_screens(src: Path, dest_dir: str, files: list[str]) -> None:
    dest = SCREENS / dest_dir
    dest.mkdir(parents=True, exist_ok=True)
    for name in files:
        target = dest / name
        if not target.exists():
            shutil.copy2(src / name, target)


# --------------------------------------------------------------------------- #
# new_samples ingestion
# --------------------------------------------------------------------------- #

def load_sample_runs(slug: str, meta: dict) -> list[dict]:
    """Turn the three seed trajectories of one task into annotation-tool runs."""
    task_dir = SAMPLES / slug
    seeds_by_num = {s["seed"]: s for s in meta.get("seeds", [])}
    runs = []

    for seed_dir in sorted(task_dir.glob("seed_[0-9]")):
        seed_num = int(seed_dir.name.rsplit("_", 1)[1])
        traj_path = seed_dir / "trajectory.jsonl"
        if not traj_path.exists():
            die(f"{slug}: missing {traj_path}")
        traj = read_json(traj_path)

        episode = f"{slug}__{seed_num}__{traj['episode_id']}"
        shot_dir = seed_dir / "screenshots"
        shots = sorted(p.name for p in shot_dir.glob("step_*.png")) if shot_dir.is_dir() else []
        copy_screens(shot_dir, episode, shots)
        have_shot = set(shots)

        steps = []
        for st in traj.get("steps", []):
            idx = st["step_idx"]
            shot_name = f"step_{idx:03d}.png"
            steps.append({
                "idx": idx,
                "action": describe_action(st.get("action_kind"), st.get("action_args")),
                "action_kind": st.get("action_kind"),
                "action_args": st.get("action_args") or {},
                "reasoning": st.get("reasoning") or "",
                "score": st.get("running_score"),
                "milestones": st.get("milestones_fired_this_step") or [],
                "url": st.get("url_after") or "",
                "img": f"screens/{episode}/{shot_name}" if shot_name in have_shot else None,
                "error": st.get("action_error"),
                "plan": st.get("raw_model_output") or "",
                "facts": st.get("facts_visible_or_created") or {},
                "snapshot": st.get("snapshot_after") or {},
                "world": compact_world(st.get("world_after")),
                "tabs": st.get("tab_strip") or [],
                "latency_ms": st.get("action_latency_ms"),
                "tokens_in": st.get("tokens_in"),
                "tokens_out": st.get("tokens_out"),
            })

        vr = traj.get("verifier_result") or {}
        seed_meta = seeds_by_num.get(seed_num, {})
        runs.append({
            "episode": episode,
            "run_id": traj["episode_id"],
            "seed": seed_num,
            "score": vr.get("score", seed_meta.get("score")),
            "success": vr.get("success", seed_meta.get("success")),
            "failure_class": traj.get("agent_failure_class"),
            "vein": traj.get("vein"),
            "specific_failure": traj.get("specific_failure") or seed_meta.get("specific_failure"),
            "missed_milestones": vr.get("missed_milestones") or [],
            "n_steps": len(steps),
            "has_log": True,
            "wave": NEW_WAVE,
            "agent": traj.get("agent_name"),
            "disposition": seed_meta.get("disposition"),
            "env": {
                "initial_url": traj.get("initial_url"),
                "initial_snapshot": traj.get("initial_snapshot") or {},
                "final_url": traj.get("final_url"),
                "final_snapshot": traj.get("final_snapshot") or {},
                "ui_variant": traj.get("ui_variant"),
                "viewport": (traj.get("image_settings") or {}).get("viewport"),
                "all_milestones": vr.get("all_milestones") or [],
                "summary_md": read_text(seed_dir / "trajectory_summary.md"),
            },
            "steps": steps,
        })

    runs.sort(key=lambda r: r["seed"])
    return runs


def load_task_env(slug: str, meta: dict) -> dict:
    """Seed payloads + factory + verifier source — the reproducibility bundle."""
    task_dir = SAMPLES / slug
    seed_index = read_json(task_dir / "seed.json") if (task_dir / "seed.json").exists() else {}
    seeds = {}
    for seed_file in sorted((task_dir / "seed_data").glob("seed_[0-9].json")):
        seeds[seed_file.stem.rsplit("_", 1)[1]] = read_json(seed_file)
    # Optional artifacts from export_env.py / export_verifiers.py; both are scoped to
    # this task alone, so nothing here can carry another task's state.
    pages = read_json(TASK_ENV / "index.json").get(slug.split("_", 1)[0], {}) if (TASK_ENV / "index.json").exists() else {}
    return {
        "pages": pages,
        "verifier_standalone": read_text(TASK_ENV / slug / "verifier_standalone.py"),
        "brief": read_text(task_dir / "brief.txt").strip(),
        "seed_factory_ref": seed_index.get("seed_factory") or meta.get("seed_source", ""),
        "seed_factory_src": read_text(task_dir / "seed_data" / "seed_factory.py"),
        "verifier_ref": meta.get("verifier_source", ""),
        "verifier_src": read_text(task_dir / "verifier.py"),
        "canonical_seed": seed_index.get("canonical_seed", 0),
        "seeds": seeds,
        "cohort": meta.get("cohort", ""),
        "cohort_notes": meta.get("cohort_notes", ""),
        "break_rate": meta.get("break_rate", ""),
        "disposition": meta.get("disposition", ""),
        "fail_reasons": meta.get("fail_reasons", []),
        "scoring": meta.get("scoring", ""),
        "provenance": {
            "traj_dir": meta.get("original_traj_dir", ""),
            "screenshot_dir": meta.get("screenshot_source_dir", ""),
            "notes": meta.get("notes", ""),
        },
    }


def merge_verifier(p1_verifier: dict, sample_verifier: dict) -> dict:
    """Phase 1 gives required/forbidden/scoring; the package gives real check source."""
    out = dict(p1_verifier or {})
    src_by_name = {m["name"]: m for m in (sample_verifier or {}).get("milestones", [])}
    milestones = []
    for m in out.get("milestones", []):
        merged = dict(m)
        extra = src_by_name.get(m["name"])
        if extra and extra.get("check_source"):
            merged["check_source"] = extra["check_source"]
        milestones.append(merged)
    seen = {m["name"] for m in milestones}
    for name, extra in src_by_name.items():
        if name not in seen:
            milestones.append({
                "name": name,
                "weight": extra.get("weight", 0.0),
                "required": extra.get("required_for_success", False),
                "forbidden": extra.get("forbidden", False),
                "hint": "",
                "check_source": extra.get("check_source", ""),
            })
    out["milestones"] = milestones
    if (sample_verifier or {}).get("scoring_notes"):
        out["scoring_notes"] = sample_verifier["scoring_notes"]
    return out


# --------------------------------------------------------------------------- #
# phase 1 ingestion
# --------------------------------------------------------------------------- #

def load_phase1_models(task: dict) -> list[dict]:
    if not INCLUDE_PHASE1_RUNS:
        return []
    models = []
    for m in task.get("models", []):
        runs = []
        for r in m.get("runs", []):
            steps = []
            for s in r.get("steps", []):
                step = dict(s)
                if step.get("img"):
                    src_img = PHASE1 / step["img"]
                    if not src_img.exists():
                        die(f"missing Phase 1 screenshot {src_img}")
                    copy_screens(src_img.parent, src_img.parent.name, [src_img.name])
                steps.append(step)
            run = dict(r)
            run["steps"] = steps
            run["wave"] = LEGACY_WAVE
            runs.append(run)
        models.append({"model": m["model"], "model_full": m.get("model_full", m["model"]), "runs": runs})
    return models


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def build() -> dict:
    if not PHASE1.exists():
        die(f"Phase 1 platform not found at {PHASE1}")
    p1 = read_json(PHASE1 / "data.json")
    p1_by_mnum = {t["mnum"]: t for t in p1["tasks"]}

    slug_by_mnum = {}
    for d in SAMPLES.iterdir():
        if d.is_dir() and (d / "task_meta.json").exists():
            slug_by_mnum[d.name.split("_", 1)[0]] = d.name

    tasks = []
    for mnum in TASK_ORDER:
        slug = slug_by_mnum.get(mnum)
        if not slug:
            die(f"{mnum} has no folder in new_samples/")
        base = p1_by_mnum.get(mnum)
        if not base:
            die(f"{mnum} is not present in the Phase 1 data.json")

        meta = read_json(SAMPLES / slug / "task_meta.json")
        models = load_phase1_models(base)
        new_runs = load_sample_runs(slug, meta)
        new_model = normalise_model(meta.get("model") or "gpt-5.5")

        target = next((m for m in models if m["model"] == new_model), None)
        if target is None:
            target = {"model": new_model, "model_full": new_model, "runs": []}
            models.append(target)
        # Wave-1 runs are the authoritative ones, so they lead the run switcher.
        target["runs"] = new_runs + target["runs"]

        rank = {name: i for i, name in enumerate(MODEL_ORDER)}
        models.sort(key=lambda m: (rank.get(m["model"], len(MODEL_ORDER)), m["model"]))

        sample_verifier = read_json(SAMPLES / slug / "verifier.json")
        tasks.append({
            "mnum": mnum,
            "slug": slug,
            "task_id": base["task_id"],
            "prompt": base["prompt"],
            "brief_agent": meta.get("brief", ""),
            "seed_link": base.get("seed_link", ""),
            "difficulty": base.get("difficulty", ""),
            "vein": base.get("vein", ""),
            "expected_behaviour": base.get("expected_behaviour", ""),
            "task_design": base.get("task_design", ""),
            "verifier": merge_verifier(base.get("verifier"), sample_verifier),
            "env": load_task_env(slug, meta),
            "models": models,
            "n_models": len(models),
            "n_runs": sum(len(m["runs"]) for m in models),
            "has_screenshots": True,
        })

    return {
        "generated": date.today().isoformat(),
        "phase": 2,
        "source": {
            "phase1": "../Traj Annotation Tool",
            "wave1_package": "new_samples",
            "wave1_model": "gpt-5.5 / openai_pixel",
        },
        "questions": p1["questions"],
        "n_tasks": len(tasks),
        "tasks": tasks,
    }


def prune_screens(data: dict) -> int:
    """Drop screenshot folders for episodes no longer referenced (e.g. retired runs)."""
    keep = {r["episode"] for t in data["tasks"] for m in t["models"] for r in m["runs"]}
    removed = 0
    if not SCREENS.exists():
        return 0
    for folder in SCREENS.iterdir():
        if folder.is_dir() and folder.name not in keep:
            shutil.rmtree(folder)
            removed += 1
    return removed


def emit(data: dict) -> None:
    (ROOT / "data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    shell = read_text(APP / "shell.html")
    app_js = read_text(APP / "app.js")
    if not shell or not app_js:
        die("app/shell.html and app/app.js are required")
    # Data is inlined rather than fetched so the page still works over file://.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (ROOT / "index.html").write_text(
        f"{shell}\n<script>\nconst DATA = {payload};\n{app_js}\n</script>\n</body>\n</html>\n",
        encoding="utf-8",
    )


def report(data: dict) -> None:
    print(f"tasks: {data['n_tasks']}")
    total_runs = total_steps = total_shots = 0
    for t in data["tasks"]:
        runs = [(m["model"], r) for m in t["models"] for r in m["runs"]]
        steps = sum(len(r["steps"]) for _, r in runs)
        shots = sum(1 for _, r in runs for s in r["steps"] if s.get("img"))
        total_runs += len(runs)
        total_steps += steps
        total_shots += shots
        models = ", ".join(f"{m['model']}×{len(m['runs'])}" for m in t["models"])
        print(f"  {t['mnum']:<5} {len(runs):>2} runs  {steps:>3} steps  {shots:>3} shots   {models}")
    print(f"totals: {total_runs} runs, {total_steps} steps, {total_shots} screenshots")
    size = (ROOT / "index.html").stat().st_size / 1e6
    print(f"index.html: {size:.1f} MB")


if __name__ == "__main__":
    d = build()
    emit(d)
    dropped = prune_screens(d)
    report(d)
    if dropped:
        print(f"pruned {dropped} screenshot folder(s) for retired runs")
