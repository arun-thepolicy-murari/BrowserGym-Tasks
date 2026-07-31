"""Prove every (task, seed) actually comes up live on the new UI.

Static checks pass trivially — data.json has 14 tasks × 3 seeds and they all
project cleanly. What matters is whether the *running* stack serves each one, so
this walks all 42 through the real bridge and asserts, per seed:

  · /bridge/reset succeeds for the task
  · the projected shop cart matches the seeded cart line-for-line
  · every gift_message and per-line ship_to_address_id survived the projection
    (these are the trap for 6 of the 14 tasks — if they vanish, the task is
    unbreakable and the annotation is worthless)
  · the mock serves the session the bridge pushed to, at the sid it reports
  · the gym's own verifier answers for the freshly-reset world, and the task's
    forbidden milestones are NOT already tripped at step 0

Run the stack first, then this:

    ./run_local.sh M73 0          # brings up gym + bridge + mocks
    _ref/venv/bin/python check_envs.py
    _ref/venv/bin/python check_envs.py --task M75 --seed 0 -v

Exit code is 0 only if all 42 pass. Leaves the last task reset, so re-run
run_local.sh for the one you actually want to annotate.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRIDGE = "http://127.0.0.1:8090"
TIMEOUT = 60  # a reset builds a whole world; be patient


def http(method: str, url: str, body: dict | None = None) -> tuple[int, object]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read().decode()
            try:
                return r.status, json.loads(raw)
            except json.JSONDecodeError:
                return r.status, raw
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:                              # connection refused etc.
        return 0, str(e)


def seeded_lines(seed_payload: dict) -> list[dict]:
    return ((seed_payload.get("cart") or {}).get("items")) or []


def audit_payloads(tasks: list[dict]) -> dict[str, list[str]]:
    """Defects visible in data.json alone — no running stack needed.

    These are packaging faults, not runtime ones, so they are checked once up front
    rather than per reset: a dangling reference or a seed that does not vary is wrong
    whether or not the mocks happen to be up.

    Grouped by kind, because two of the three findings hold for nearly every task —
    printed flat they are 27 lines of noise that bury the one defect that is specific
    to a single task.
    """
    flat_seed: list[str] = []
    stale_prompt: list[str] = []
    dangling: list[str] = []
    for t in tasks:
        env = t.get("env") or {}
        seeds = env.get("seeds") or {}
        keys = sorted(seeds)

        # (1) Seeds that do not actually differ. The gym factories take `seed` but most
        # of the wave-1 ones never branch on it, so "3 seeds" can be one world reviewed
        # three times. Worth knowing before anyone budgets 42 reviews.
        def canon(k: str) -> str:
            return json.dumps(seeds[k], sort_keys=True,
                              default=str).replace(f'"seed": {k}', '"seed": _')
        if len(keys) > 1 and len({canon(k) for k in keys}) == 1:
            flat_seed.append(t["mnum"])

        # (2) References that point at nothing in the packaged payload.
        for k in keys:
            sd = seeds[k]
            prods, addrs = sd.get("products") or {}, sd.get("addresses") or {}
            for line in seeded_lines(sd):
                if line.get("product_id") not in prods:
                    dangling.append(f"{t['mnum']} seed {k}: cart line {line.get('id')} references "
                                    f"product {line.get('product_id')!r}, absent from the catalogue")
                sa = line.get("ship_to_address_id")
                if sa and sa not in addrs:
                    dangling.append(f"{t['mnum']} seed {k}: cart line {line.get('id')} ships to "
                                    f"{sa!r}, absent from addresses")
            for o in sd.get("orders_at_seed") or []:
                for it in o.get("items") or []:
                    if it.get("product_id") not in prods:
                        dangling.append(
                            f"{t['mnum']} seed {k}: order {o.get('id')} references product "
                            f"{it.get('product_id')!r}, absent from the catalogue — its name, "
                            f"price and order detail are not reviewable")

        # (3) The header brief an annotator grades against must be the words the agent
        # actually got, not a paraphrase.
        brief, prompt = (env.get("brief") or "").strip(), (t.get("prompt") or "").strip()
        if brief and prompt and brief != prompt:
            stale_prompt.append(t["mnum"])

    return {"dangling reference": dangling, "seeds do not vary": flat_seed,
            "stale `prompt` field": stale_prompt}


def check(task: dict, seed: str, verbose: bool) -> list[str]:
    """Problems found for one (task, seed). Empty list == healthy."""
    mnum, task_id = task["mnum"], task["task_id"]
    tag = f"{mnum} seed {seed}"
    bad: list[str] = []

    status, r = http("POST", f"{BRIDGE}/bridge/reset",
                     {"task_id": task_id, "seed": int(seed)})
    if status != 200 or not isinstance(r, dict) or not r.get("ok"):
        return [f"{tag}: bridge reset failed ({status}) {str(r)[:200]}"]

    apps = {k: v for k, v in (r.get("apps") or {}).items() if v}
    sids, mocks = r.get("sids") or {}, r.get("mocks") or {}
    if "shop" not in apps:
        bad.append(f"{tag}: engine produced no shop state")
        return bad
    if "shop" not in sids:
        bad.append(f"{tag}: bridge pushed nothing to the shop mock "
                   f"(CUA_HUB_URL_SHOP set? mock up?)")

    # --- the projection must not drop cart-line options -----------------------
    want = seeded_lines((task.get("env") or {}).get("seeds", {}).get(seed) or {})
    got = (apps["shop"] or {}).get("cart") or []
    if len(got) != len(want):
        bad.append(f"{tag}: cart has {len(got)} line(s), seed defines {len(want)}")
    for field in ("gift_message", "ship_to_address_id", "scheduled_delivery", "gift_wrap"):
        w = sum(1 for i in want if i.get(field))
        g = sum(1 for l in got if l.get(field))
        if g != w:
            bad.append(f"{tag}: {field} — seed has {w}, projection has {g} "
                       f"(the trap is being erased before the annotator sees it)")
    if want and not all(l.get("lineId") for l in got):
        bad.append(f"{tag}: a projected cart line has no lineId, so a click "
                   f"cannot address the exact line")

    # --- dated artifacts must still be visible in the mock's own UI ----------
    # amazon_mock's Orders page filters on the REAL clock and opens on "past 3 months",
    # while the gym world is frozen at SEED_DATE. An order outside that window is not an
    # error anywhere — it just silently isn't rendered, and the task's premise evaporates
    # (M111 is "my kettle never arrived"; the proof it did is that order).
    now = datetime.datetime.now(datetime.timezone.utc)
    for o in (apps["shop"] or {}).get("orders") or []:
        raw = o.get("date")
        if not raw:
            continue
        try:
            when = datetime.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except ValueError:
            bad.append(f"{tag}: order {o.get('id')} has an unparseable date {raw!r}")
            continue
        age = (now - when).days
        if age > 90:
            bad.append(f"{tag}: order {o.get('id')} is dated {str(raw)[:10]} ({age}d ago) — "
                       f"outside the Orders page's default 'past 3 months' tab, so it is "
                       f"invisible unless the annotator switches tabs. Rebase the clock "
                       f"(GYM_DATE_REBASE) or the environment misrepresents itself.")
        elif age > 75:
            bad.append(f"{tag}: order {o.get('id')} is {age}d old — within {90 - age} day(s) "
                       f"of dropping off the default Orders tab.")

    # --- the mock must actually serve the session the bridge wrote ------------
    base, sid = mocks.get("shop"), sids.get("shop")
    if base and sid:
        q = urllib.parse.urlencode({"sid": sid})
        st, body = http("GET", f"{base.rstrip('/')}/state?{q}")
        if st != 200:
            bad.append(f"{tag}: mock /state?sid returned {st} for {sid}")
        elif isinstance(body, dict):
            served = body if "cart" in body else (body.get("state") or {})
            # Compare what the MOCK holds against what the engine projected. If these
            # diverge the browser is showing the mock's own demo data, which looks
            # plausible and is entirely wrong — the failure mode worth catching.
            sc = served.get("cart")
            if sc is not None and len(sc) != len(got):
                bad.append(f"{tag}: mock serves {len(sc)} cart line(s), engine projected "
                           f"{len(got)} — the tab is showing unseeded demo data")
            so = served.get("orders")
            eo = (apps["shop"] or {}).get("orders") or []
            if so is not None and len(so) != len(eo):
                bad.append(f"{tag}: mock serves {len(so)} order(s), engine projected "
                           f"{len(eo)} — pre-existing orders are missing from the UI")
            for eline in got:
                match = next((l for l in (sc or []) if l.get("productId") == eline.get("productId")), None)
                if match is None:
                    bad.append(f"{tag}: product {eline.get('productId')} missing from the mock's cart")
                    continue
                for field in ("gift_message", "ship_to_address_id"):
                    if (eline.get(field) or "") != (match.get(field) or ""):
                        bad.append(f"{tag}: {field} on {eline.get('productId')} is "
                                   f"{match.get(field)!r} in the mock, {eline.get(field)!r} in the engine")

    # --- nothing forbidden may already be tripped at step 0 ------------------
    st, v = http("GET", f"{BRIDGE}/bridge/verify")
    if st != 200 or not isinstance(v, dict):
        bad.append(f"{tag}: /bridge/verify returned {st}")
    else:
        ms = v.get("milestones") or v.get("results") or []
        tripped = [m.get("name") for m in ms
                   if isinstance(m, dict) and m.get("forbidden") and m.get("hit")]
        if tripped:
            bad.append(f"{tag}: forbidden milestone(s) already tripped at step 0: "
                       f"{tripped} — the seed is not a clean starting state")
        if verbose:
            print(f"    verify: {len(ms)} milestone(s), score {v.get('score')}")

    if verbose:
        gm = sum(1 for l in got if l.get("gift_message"))
        print(f"    apps={sorted(apps)} cart={len(got)} giftMsg={gm} sid={sid}")
    return bad


def main(argv: list[str] | None = None) -> int:
    global BRIDGE
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bridge", default=BRIDGE)
    ap.add_argument("--task", help="limit to one MNUM, e.g. M75")
    ap.add_argument("--seed", help="limit to one seed")
    ap.add_argument("--payload-only", action="store_true",
                    help="audit data.json only; needs no running stack")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    BRIDGE = args.bridge.rstrip("/")

    tasks = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))["tasks"]
    if args.task:
        tasks = [t for t in tasks if t["mnum"].upper() == args.task.upper()]
        if not tasks:
            print(f"unknown task {args.task}", file=sys.stderr)
            return 2

    print("payload audit")
    groups = audit_payloads(tasks)
    if not any(groups.values()):
        print(f"  ok   {len(tasks)} task payload(s) clean")
    for kind, hits in groups.items():
        if not hits:
            continue
        if kind == "dangling reference":
            for h in hits:                       # task-specific — print each in full
                print(f"  warn {h}")
        elif kind == "seeds do not vary":
            print(f"  warn seeds identical on {len(hits)}/{len(tasks)} task(s): "
                  f"{', '.join(hits)}")
            print( "       the factories take `seed` but never branch on it, so each "
                   "task's 3 runs replay one world")
        else:
            print(f"  warn stale `prompt` on {len(hits)}/{len(tasks)} task(s): "
                  f"{', '.join(hits)}")
            print( "       the UI grades against env.brief (the agent's actual words); "
                   "the `prompt` field is a Phase 1 paraphrase")
    print()

    if args.payload_only:
        # Payload defects are reported but do not fail the run: they are known
        # upstream properties of the wave-1 package, not regressions in this repo.
        return 0

    st, _ = http("GET", f"{BRIDGE}/bridge/actions")
    if st != 200:
        print(f"bridge is not answering at {BRIDGE} — run ./run_local.sh first "
              f"(or pass --payload-only)", file=sys.stderr)
        return 2

    print("live environment")
    problems: list[str] = []
    n = 0
    for t in tasks:
        seeds = sorted((t.get("env") or {}).get("seeds") or {})
        if args.seed:
            seeds = [s for s in seeds if s == str(args.seed)]
        for s in seeds:
            n += 1
            found = check(t, s, args.verbose)
            problems += found
            print(f"  {'FAIL' if found else 'ok  '} {t['mnum']} seed {s}")
            for p in found:
                print(f"       {p}")

    print()
    if problems:
        print(f"{len(problems)} problem(s) across {n} task/seed(s)")
        return 1
    print(f"all {n} task/seed(s) live and intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
