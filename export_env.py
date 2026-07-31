#!/usr/bin/env python3
"""Export a per-task static snapshot of the gym UI, one isolated folder per task.

The gym serves a single global world, so seeding task B overwrites task A's state.
This exporter therefore resets the world immediately before rendering each
(task, seed) and writes the result into its own directory:

    task_env/
      _static/                       shared css/js (no task state)
      M73_expired_card_checkout/
        seed_0/cart.html, checkout_address.html, ...
        seed_1/ ...  seed_2/ ...
      M75_stale_gift_message/ ...

Nothing is shared between task folders, so one task's cart, orders or gift messages
can never appear inside another task's environment.

Pages are captured at the *seeded* starting state — what the agent saw at step 0.
Order-confirmation pages are skipped: those are artifacts the agent created during a
run, not part of the environment.

Run with the gym's Python (needs fastapi/jinja2):

    _ref/venv/bin/python export_env.py
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
GYM = ROOT / "browser-gym-seed-to-cua-gym"
SAMPLES = ROOT / "new_samples"
OUT = ROOT / "task_env"
SEEDS = (0, 1, 2)

# Pages worth capturing for every task: the checkout funnel and the account screens
# where the traps (expired card, address book, gift message) are visible.
BASE_PAGES = [
    "/cart",
    "/checkout/address",
    "/checkout/payment",
    "/checkout/review",
    "/account/payments",
    "/account/addresses",
    "/account/orders",
]
# Paths that only exist because an agent created them during a run.
RUN_ARTIFACT = re.compile(r"^/(order-confirmation|order)/")

sys.path.insert(0, str(GYM))
os.environ.setdefault("HARNESS_TOKEN", "export-token")
HEADERS = {"X-Harness-Token": os.environ["HARNESS_TOKEN"]}


def page_filename(path: str) -> str:
    """`/checkout/address` -> `checkout_address.html`, `/` -> `home.html`."""
    clean = path.strip("/")
    if not clean:
        return "home.html"
    return re.sub(r"[^a-zA-Z0-9]+", "_", clean).strip("_") + ".html"


def task_paths(task: dict) -> list[str]:
    """Base pages plus any extra page this task's own trajectories actually visited."""
    extra = []
    for model in task["models"]:
        for run in model["runs"]:
            for step in run["steps"]:
                url = step.get("url") or ""
                if not url:
                    continue
                path = urlsplit(url).path or "/"
                if RUN_ARTIFACT.match(path):
                    continue
                if path not in BASE_PAGES and path not in extra:
                    extra.append(path)
    return BASE_PAGES + sorted(extra)


def rewrite(html: str, exported: dict[str, str], depth: int) -> str:
    """Point assets and in-page links at the static export instead of the server."""
    up = "../" * depth
    html = html.replace('href="/static/', f'href="{up}_static/')
    html = html.replace('src="/static/', f'src="{up}_static/')

    def link(m: re.Match) -> str:
        attr, path = m.group(1), m.group(2)
        target = exported.get(path.rstrip("/") or "/")
        if target:
            return f'{attr}="{target}"'
        # Not part of this task's snapshot — keep it inert rather than 404.
        return f'{attr}="#" data-offline="{path}" title="not part of this task snapshot"'

    html = re.sub(r'(href)="(/(?!static/)[^"#?]*)"', link, html)
    # The bridge client would try to POST to a server that isn't there.
    html = re.sub(r'<script[^>]*\bsrc="[^"]*bridge[^"]*"[^>]*>\s*</script>', "", html)
    return html


def add_banner(html: str, label: str, seed: int) -> str:
    banner = (
        '<div style="position:sticky;top:0;z-index:9999;background:#12305f;color:#8db4ff;'
        'font:12px/1.5 ui-monospace,Menlo,monospace;padding:6px 12px;border-bottom:1px solid #1b498f">'
        f"STATIC SNAPSHOT — {label} at seed {seed}. Read-only: buttons and forms do not submit."
        "</div>"
    )
    return re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + banner, html, count=1)


def export_task(client, slug: str, task_id: str, task: dict, report: list) -> dict:
    paths = task_paths(task)
    per_seed: dict[str, list[dict]] = {}

    for seed in SEEDS:
        # A fresh reset per (task, seed) is what keeps snapshots from bleeding together.
        r = client.post(
            "/_harness/reset", json={"task_id": task_id, "seed": seed}, headers=HEADERS
        )
        if r.status_code != 200:
            report.append(f"{slug} seed {seed}: reset failed ({r.status_code})")
            continue
        start_path = (r.json() or {}).get("start_path") or "/cart"

        wanted = list(dict.fromkeys([start_path] + paths))
        exported = {p: page_filename(p) for p in wanted}
        dest = OUT / slug / f"seed_{seed}"
        dest.mkdir(parents=True, exist_ok=True)

        pages = []
        for path in wanted:
            resp = client.get(path, follow_redirects=True)
            if resp.status_code != 200 or "text/html" not in resp.headers.get("content-type", ""):
                report.append(f"{slug} seed {seed}: {path} -> {resp.status_code}")
                continue
            html = add_banner(rewrite(resp.text, exported, depth=2), f"{slug} · {path}", seed)
            (dest / exported[path]).write_text(html, encoding="utf-8")
            pages.append({
                "path": path,
                "file": f"task_env/{slug}/seed_{seed}/{exported[path]}",
                "start": path == start_path,
            })
        per_seed[str(seed)] = pages

    return per_seed


def main() -> int:
    import warnings

    warnings.filterwarnings("ignore")
    from fastapi.testclient import TestClient
    from server.main import app

    data_path = ROOT / "data.json"
    if not data_path.exists():
        sys.exit("export_env: run build.py first (data.json is missing)")
    data = json.loads(data_path.read_text(encoding="utf-8"))

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(GYM / "ui" / "static", OUT / "_static")

    client = TestClient(app)
    report: list[str] = []
    index = {}
    for task in data["tasks"]:
        slug = task["slug"]
        per_seed = export_task(client, slug, task["task_id"], task, report)
        index[task["mnum"]] = per_seed
        n = sum(len(v) for v in per_seed.values())
        print(f"  {task['mnum']:<5} {n:>3} pages across {len(per_seed)} seeds")

    (OUT / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT}")
    if report:
        print(f"\n{len(report)} page(s) skipped:")
        for line in report[:25]:
            print("  -", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
