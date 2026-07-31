"""Trace one (task, seed) through every layer and print where the data stops.

There are four places an order can go missing between the gym and the pixels, and
they all look identical in a browser:

  1. the gym engine        GET  {gym}/_harness/world_full   -> shop.orders
  2. the bridge projection GET  {bridge}/bridge/state?app=shop -> orders[]
  3. the mock's session    GET  {mock}/state?sid=<sid>       -> orders[]
  4. the page in the tab   whether it is in bridged mode at all

Layer 4 is the sneaky one. amazon_mock decides bridged-vs-legacy from
`?bridge=` in `location.search`, read ONCE at module load. Any full page load
without that param — a reload, a bookmark, a real <a href> rather than a
react-router <Link> — silently drops the tab into legacy mode, where it renders
the mock's own demo catalogue. That looks completely plausible and is entirely
not your task.

Run it with the stack up:

    ./run_local.sh M111 0
    python3 diagnose_m111.py                 # defaults to M111 seed 0
    python3 diagnose_m111.py --task M75 --seed 1
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def get(url: str, headers: dict | None = None, timeout: int = 30):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            try:
                return r.status, json.loads(raw)
            except json.JSONDecodeError:
                return r.status, raw
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]
    except Exception as e:
        return 0, str(e)


def orders_of(state) -> list:
    if not isinstance(state, dict):
        return []
    if isinstance(state.get("orders"), list):
        return state["orders"]
    inner = state.get("state")
    return inner.get("orders", []) if isinstance(inner, dict) else []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="M111")
    ap.add_argument("--seed", default=None, help="defaults to whatever is live")
    ap.add_argument("--bridge", default="http://127.0.0.1:8090")
    args = ap.parse_args()
    bridge = args.bridge.rstrip("/")

    live = {}
    p = ROOT / "live_env.json"
    if p.exists():
        live = json.loads(p.read_text())
    seed = args.seed if args.seed is not None else str(live.get("seed", 0))

    print(f"live_env.json : {live.get('mnum')} seed {live.get('seed')} "
          f"mode={live.get('mode')} route_style={live.get('route_style')}")
    if live.get("mnum") and live["mnum"] != args.task:
        print(f"  !! {args.task} is NOT the live task — reset it first, or the layers below "
              f"describe {live['mnum']}")
    print()

    # -- layer 2: what the bridge projects -----------------------------------
    st, body = get(f"{bridge}/bridge/state?app=shop")
    if st != 200:
        print(f"2. bridge projection : UNREACHABLE ({st}) {str(body)[:120]}")
        print("   -> the stack is not running; ./run_local.sh first")
        return 2
    proj = (body.get("apps") or {}).get("shop") or {}
    po = orders_of(proj)
    print(f"2. bridge projection : {len(po)} order(s), {len(proj.get('cart') or [])} cart line(s), "
          f"{len(proj.get('products') or [])} products")
    for o in po:
        print(f"     {o.get('id')}  {str(o.get('date'))[:10]}  {o.get('status')}  ${o.get('total')}  "
              f"items={[i.get('productId') for i in (o.get('items') or [])]}")
    for o in po:
        for i in o.get("items") or []:
            if not any(pr.get("id") == i.get("productId") for pr in proj.get("products") or []):
                print(f"     !! {i.get('productId')} is not in the projected catalogue — "
                      f"the Orders row will render without a name or image")

    # -- layer 3: what the mock actually holds under the sid -----------------
    sid = (live.get("sids") or {}).get("shop")
    shop_url = (live.get("apps") or {}).get("shop") or "http://127.0.0.1:5201/"
    parts = urllib.parse.urlsplit(shop_url)
    mock = f"{parts.scheme}://{parts.netloc}"        # origin only, drop /cart?sid=…#/cart
    print()
    if not sid:
        print("3. mock session      : no sid in live_env.json — cannot check")
    else:
        st, body = get(f"{mock}/state?{urllib.parse.urlencode({'sid': sid})}")
        mo = orders_of(body)
        print(f"3. mock session      : {mock}/state?sid={sid}")
        print(f"                       HTTP {st}, {len(mo)} order(s)")
        if st == 200 and len(mo) != len(po):
            print(f"     !! mock has {len(mo)} order(s), bridge projects {len(po)} — "
                  f"the push did not land, or something re-wrote the session")

    # -- layer 4: is the tab even bridged ------------------------------------
    print()
    q = urllib.parse.parse_qs(parts.query)
    print(f"4. the URL you open  : {shop_url or '(none)'}")
    print(f"     carries ?bridge= : {'yes' if q.get('bridge') else 'NO — the tab will run in legacy demo mode'}")
    print(f"     carries ?sid=    : {'yes' if q.get('sid') else 'no'}")
    print()
    print("   amazon_mock reads ?bridge= from location.search ONCE, at module load.")
    print("   If the Orders page was reached by a full page load that dropped the query")
    print("   string (reload, bookmark, typing /orders, or a plain <a href>), the tab is")
    print("   in LEGACY mode and is showing the mock's built-in demo data — which has no")
    print("   ORD-KT-111 and no Electric Kettle. Check the address bar of the tab that is")
    print("   missing the order: if there is no ?bridge= in it, that is the whole story.")
    print()
    print("   Test: open the Orders page from the launcher link, then edit the address bar")
    print(f"   to  {mock}/orders?{urllib.parse.urlencode({'sid': sid or 'SID', 'bridge': bridge})}")
    print("   If the order appears, it is layer 4 and the fix is to keep the params on")
    print("   every navigation, not to touch the seed data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
