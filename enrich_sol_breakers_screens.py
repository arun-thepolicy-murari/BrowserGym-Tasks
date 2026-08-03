#!/usr/bin/env python3
"""Populate Sol Breakers runs with curated step screenshots (wave-1 schema).

Reads trajectory JSONL + PNGs from browser-gym-seed-to-cua-gym, copies a
modest curated set into ``screens/<episode>/``, and rewrites
``sol_breakers/tasks.json`` so each run has the same ``steps`` / ``img`` shape
as Wave-1 QA cards.

Usage:
  python3 enrich_sol_breakers_screens.py
  python3 merge_sol_breakers.py
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOL_PKG = ROOT / "sol_breakers" / "tasks.json"
SCREENS = ROOT / "screens"

# Prefer the sibling seed-to-cua checkout (full screenshot tree).
CANDIDATE_GYMS = [
    ROOT.parent / "browser-gym-seed-to-cua-gym",
    Path("/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym"),
    ROOT.parent / "ecommerce-browser-gym",
    Path("/Users/maroonferrari/Deccan/ecommerce-browser-gym"),
]

# Wave-1 averages ~10–11 steps/run (max 39). Cap Sol curation near that.
MAX_STEPS_PER_RUN = 12

# Frames a card's copy points at that no milestone fires on, so even sampling can
# drop them. Keyed by episode.
PINNED_STEPS: dict[str, tuple[int, ...]] = {
    # n7 seed 0: read Your Orders (26), then re-demanded the refund calling those
    # details "verified order details" (33).
    "mail_003_false_double_charge__0__8be6f888": (26, 32, 33),
}


def describe_action(kind: str, args: dict) -> str:
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
                k: v
                for k, v in app_state.items()
                if v not in (None, "", [], {}, 0, False)
                and k not in ("task_id", "seed", "step", "finished")
            }
            if trimmed:
                out[app_name] = trimmed
    return out


def find_gym() -> Path:
    for p in CANDIDATE_GYMS:
        if (p / "screenshots").is_dir() and (p / "trajectories").is_dir():
            return p
    raise SystemExit("No gym checkout with screenshots/ + trajectories/ found")


def read_json(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_traj(gym: Path, episode: str, provenance: dict) -> Path:
    """Locate the JSONL for an episode using provenance hints + glob."""
    name = f"{episode}.jsonl"
    # Prefer directories named in provenance.traj_dir.
    hints = []
    traj_dir = (provenance or {}).get("traj_dir") or ""
    # e.g. "browser-gym-seed-to-cua-gym/trajectories/lh_004_once_its_done_sol_seed0/"
    m = re.search(r"trajectories/([^/\s]+)", traj_dir)
    if m:
        hints.append(m.group(1).rstrip(")"))
    # Parenthetical alt dirs: "(seed0 also cal_004_bridged_confirm/)"
    for alt in re.findall(r"([a-z0-9_]+(?:_confirm|_seed0|_3seed)?)/?", traj_dir, re.I):
        if alt not in hints and "trajector" not in alt:
            hints.append(alt)

    for hint in hints:
        candidate = gym / "trajectories" / hint / name
        if candidate.exists():
            return candidate

    matches = list((gym / "trajectories").rglob(name))
    if not matches:
        # Episode folder name sometimes differs from jsonl stem location.
        matches = list((gym / "trajectories").rglob(f"*{episode.split('__')[-1]}*.jsonl"))
    if not matches:
        raise FileNotFoundError(f"No JSONL for episode {episode}")
    # Prefer paths that contain the episode stem.
    exact = [p for p in matches if p.name == name]
    if exact:
        return exact[0]
    return matches[0]


def resolve_shot_dir(gym: Path, episode: str, traj: dict) -> Path:
    steps = traj.get("steps") or []
    if steps and steps[0].get("screenshot_path"):
        rel = Path(steps[0]["screenshot_path"]).parent
        candidate = gym / rel
        if candidate.is_dir():
            return candidate
    matches = list((gym / "screenshots").rglob(episode))
    dirs = [p for p in matches if p.is_dir()]
    if not dirs:
        raise FileNotFoundError(f"No screenshot dir for {episode}")
    return dirs[0]


def curate_indices(
    steps: list[dict],
    max_keep: int = MAX_STEPS_PER_RUN,
    pinned: tuple[int, ...] = (),
) -> list[int]:
    n = len(steps)
    if n <= max_keep:
        return list(range(n))

    must: set[int] = {0, n - 1}
    must.update(i for i in pinned if 0 <= i < n)
    for st in steps:
        idx = int(st["step_idx"])
        ms = st.get("milestones_fired_this_step") or []
        if ms:
            must.add(idx)
            if idx - 1 >= 0:
                must.add(idx - 1)
            if idx + 1 < n:
                must.add(idx + 1)

    # Prefer forbidden / break-ish milestone names if we somehow exceed budget.
    if len(must) > max_keep:
        core = {0, n - 1}
        core.update(i for i in pinned if 0 <= i < n)
        for st in steps:
            idx = int(st["step_idx"])
            ms = st.get("milestones_fired_this_step") or []
            if any(
                any(
                    tok in (m or "").lower()
                    for tok in (
                        "forbidden",
                        "paid_expired",
                        "bought_",
                        "silent_double",
                        "emailed_support",
                    )
                )
                for m in ms
            ):
                core.add(idx)
        # Fill remaining slots with other musts then drop extras.
        ordered = sorted(core) + [i for i in sorted(must) if i not in core]
        return sorted(ordered[:max_keep])

    keep = set(must)
    # Evenly sample remaining slots across the trajectory.
    remaining = max_keep - len(keep)
    if remaining > 0:
        candidates = [i for i in range(n) if i not in keep]
        if candidates:
            # Inclusive spacing across candidate list.
            if remaining >= len(candidates):
                keep.update(candidates)
            else:
                for j in range(remaining):
                    pos = round(j * (len(candidates) - 1) / max(remaining - 1, 1))
                    keep.add(candidates[pos])
    return sorted(keep)


def build_step(st: dict, episode: str, have_shot: set[str]) -> dict:
    idx = int(st["step_idx"])
    shot_name = f"step_{idx:03d}.png"
    return {
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
    }


def enrich_run(run: dict, gym: Path, provenance: dict) -> dict:
    episode = run["episode"]
    traj_path = resolve_traj(gym, episode, provenance)
    traj = read_json(traj_path)
    all_steps = traj.get("steps") or []
    keep = curate_indices(all_steps, pinned=PINNED_STEPS.get(episode, ()))

    shot_src: Path | None = None
    try:
        shot_src = resolve_shot_dir(gym, episode, traj)
    except FileNotFoundError as exc:
        print(f"  WARN skip screens for {episode}: {exc}")

    dest = SCREENS / episode
    dest.mkdir(parents=True, exist_ok=True)
    have_shot: set[str] = set()
    if shot_src is not None:
        for idx in keep:
            name = f"step_{idx:03d}.png"
            src = shot_src / name
            if not src.exists():
                continue
            target = dest / name
            if not target.exists() or target.stat().st_size != src.stat().st_size:
                shutil.copy2(src, target)
            have_shot.add(name)

    curated = [build_step(all_steps[i], episode, have_shot) for i in keep if i < len(all_steps)]
    out = dict(run)
    out["steps"] = curated
    out["n_steps"] = len(curated)
    out["has_log"] = True
    # Preserve existing env summary; add traj bookends when missing.
    env = dict(out.get("env") or {})
    env.setdefault("initial_url", traj.get("initial_url"))
    env.setdefault("initial_snapshot", traj.get("initial_snapshot") or {})
    env.setdefault("final_url", traj.get("final_url"))
    env.setdefault("final_snapshot", traj.get("final_snapshot") or {})
    env.setdefault("ui_variant", traj.get("ui_variant"))
    env.setdefault("viewport", (traj.get("image_settings") or {}).get("viewport"))
    vr = traj.get("verifier_result") or {}
    if not env.get("all_milestones") and vr.get("all_milestones"):
        env["all_milestones"] = vr["all_milestones"]
    out["env"] = env
    if out.get("score") is None and "score" in vr:
        out["score"] = vr["score"]
    if out.get("success") is None and "success" in vr:
        out["success"] = vr["success"]
    return out


def main() -> None:
    gym = find_gym()
    pkg = read_json(SOL_PKG)
    total_shots = 0
    for task in pkg.get("tasks") or []:
        provenance = (task.get("env") or {}).get("provenance") or {}
        models = task.get("models") or []
        any_shots = False
        for model in models:
            new_runs = []
            for run in model.get("runs") or []:
                enriched = enrich_run(run, gym, provenance)
                new_runs.append(enriched)
                n_img = sum(1 for s in enriched["steps"] if s.get("img"))
                total_shots += n_img
                any_shots = any_shots or n_img > 0
                print(
                    f"  {task['mnum']} seed{enriched['seed']}: "
                    f"{enriched['n_steps']} curated steps "
                    f"({n_img} png) ← {enriched['episode']}"
                )
            model["runs"] = new_runs
        task["has_screenshots"] = any_shots
        # Point annotators at the packaged screens + source tree.
        provenance = dict((task.get("env") or {}).get("provenance") or {})
        provenance["screenshot_dir"] = f"screens/<episode>/ (curated from {gym.name}/screenshots/)"
        provenance["notes"] = (
            "Step screenshots curated into screens/<episode>/ (trap + key UI frames; "
            f"≤{MAX_STEPS_PER_RUN}/run). Same step schema as Wave-1 QA."
        )
        task.setdefault("env", {})["provenance"] = provenance

    pkg["notes"] = (
        (pkg.get("notes") or "").rstrip()
        + " Screenshots packaged 2026-08-03: curated ≤"
        + str(MAX_STEPS_PER_RUN)
        + " frames/run from seed-to-cua-gym trajectories into screens/."
    )
    # Avoid duplicating the note on re-runs.
    if pkg["notes"].count("Screenshots packaged") > 1:
        parts = pkg["notes"].split(" Screenshots packaged")
        pkg["notes"] = parts[0] + " Screenshots packaged" + parts[-1]

    write_json(SOL_PKG, pkg)
    print(f"gym: {gym}")
    print(f"wrote {SOL_PKG}")
    print(f"total curated png refs: {total_shots}")
    print(f"screens/: {(SCREENS).resolve()}")


if __name__ == "__main__":
    main()
