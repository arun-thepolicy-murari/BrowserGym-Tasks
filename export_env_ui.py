#!/usr/bin/env python3
"""Build CUA mock UIs into env_ui/ and export per-task shop seed JSON.

Built assets use Vite base './' + HashRouter so they work on GitHub Pages and local
http.server without a bridge.

Seed state comes from the gym's own `transform_shop` wherever the gym is importable,
so the static Pages environment and the live bridged one are produced by ONE code
path. They used to be two: this file carried its own copy of the transform, fed from
the packaged `new_samples/*/seed_data/*.json` rather than the live world, and it
quietly disagreed with the real thing —

  * order dates were hardcoded to `2024-01-01`, which is ~940 days before any real
    "today". amazon_mock's Orders page filters on the wall clock and opens on the
    "past 3 months" tab, so every pre-existing order rendered as an EMPTY page. That
    is the whole of M111: its brief is "my electric kettle order never showed up",
    and the order proving it did was invisible.
  * `total` came from `orders_at_seed`, which has no `total` key -> null.
  * `products` came from the packaged seed's filtered catalogue, so an order line
    could reference a product that was not there (M111's `p_kettle_111`) and render
    with no name, price or image.

The packaged-payload path is kept as a fallback for building without the gym, but it
warns, because what it produces is a degraded environment rather than a faithful one.
"""
from __future__ import annotations

import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HUB = ROOT / "CUA-Gym-Hub" / "websites"
OUT = ROOT / "env_ui"
SAMPLES = ROOT / "new_samples"
GYM = ROOT / "browser-gym-seed-to-cua-gym"

# The gym's world is frozen here; the mocks render against the real clock.
SEED_DATE = datetime.date(2026, 5, 21)


def _gym():
    """The gym's canonical transform, or None if this checkout can't import it."""
    if str(GYM) not in sys.path:
        sys.path.insert(0, str(GYM))
    try:
        from tools.seed_to_cuagym import dump_world, transform_shop
        return dump_world, transform_shop
    except Exception as exc:                       # no gym, no venv, no deps
        print(f"  !! gym not importable ({exc.__class__.__name__}: {exc})", file=sys.stderr)
        return None

# mock dir name -> env_ui folder
APPS = {
    "shop": "amazon_mock",
    "mail": "gmail_mock",
    "market": "ebay_mock",
    "food": "uber_eats_mock",
}


def picsum(pid: str) -> str:
    return f"https://picsum.photos/seed/{pid}/400/400"


def pack_to_shop(seed: dict) -> dict:
    """wave-1 seed_data JSON -> amazon_mock state."""
    products = []
    for p in (seed.get("products") or {}).values():
        stock = p.get("stock") or 0
        products.append({
            "id": p["id"],
            "title": p.get("name"),
            "price": p.get("base_price"),
            "originalPrice": None,
            "rating": p.get("rating"),
            "reviewCount": p.get("review_count"),
            "image": picsum(p["id"]),
            "images": [picsum(p["id"])],
            "description": p.get("long_description") or p.get("short_description") or "",
            "bulletPoints": p.get("tags") or [],
            "specs": {"Brand": p.get("brand"), "Emoji": p.get("image_emoji")},
            "category": "Home & Kitchen" if (p.get("category") or "").lower() in ("home", "kitchen") else "Electronics",
            "brand": p.get("brand"),
            "prime": True,
            "inStock": stock > 0,
            "stockCount": stock,
            "seller": "Amazon.com",
            "badges": (["Best Seller"] if (p.get("rating") or 0) >= 4.5 else []),
            "createdAt": "2024-01-01T00:00:00.000Z",
        })

    addrs = []
    for a in (seed.get("addresses") or {}).values():
        addrs.append({
            "id": a["id"],
            "label": a.get("label") or "Home",
            "name": a.get("full_name") or "Alice Anderson",
            "line1": a.get("line1") or "",
            "line2": a.get("line2") or "",
            "city": a.get("city") or "",
            "state": a.get("state") or "",
            "zip": a.get("zip") or "",
            "isDefault": bool(a.get("is_default")),
        })
    pays = []
    for p in (seed.get("payment_methods") or {}).values():
        pays.append({
            "id": p["id"],
            "type": "paypal" if (p.get("kind") or "") == "paypal" else "card",
            "label": p.get("label") or p["id"],
            "last4": (p.get("label") or "****")[-4:] if "****" in (p.get("label") or "") else "4242",
            "expiry": p.get("expires") or "",
            "isDefault": bool(p.get("is_default")),
        })
    if not addrs:
        addrs = [{"id": "addr_home", "label": "Home", "name": "Alice Anderson",
                  "line1": "100 Park Avenue", "line2": "", "city": "Brooklyn",
                  "state": "NY", "zip": "11201", "isDefault": True}]
    if not pays:
        pays = [{"id": "pay_visa", "type": "card", "label": "Visa ****4242",
                 "last4": "4242", "expiry": "04/26", "isDefault": True}]
    def_addr = next((a for a in addrs if a["isDefault"]), addrs[0])
    def_pay = next((p for p in pays if p["isDefault"]), pays[0])
    user = {
        "id": "u1", "name": def_addr.get("name", "Alice Anderson"),
        "email": "alice@example.com",
        "address": def_addr, "addresses": addrs,
        "paymentMethod": def_pay, "paymentMethods": pays,
    }

    cart = []
    for it in ((seed.get("cart") or {}).get("items") or []):
        line = {
            "productId": it.get("product_id"),
            "quantity": it.get("quantity") or 1,
            "lineId": it.get("id"),
        }
        for k in ("gift_wrap", "gift_message", "ship_to_address_id", "scheduled_delivery"):
            if it.get(k) not in (None, "", False):
                line[k] = it[k]
        cart.append(line)

    # A hardcoded date here is what made every pre-existing order invisible. Without
    # the gym we have no `placed_at`, so put the order a plausible few days back from
    # today — visible in the default tab, which is the property that matters.
    fallback_date = (datetime.datetime.now() - datetime.timedelta(days=9)) \
        .strftime("%Y-%m-%dT%H:%M:%S.000Z")
    orders = []
    for o in seed.get("orders_at_seed") or []:
        orders.append({
            "id": o.get("id"),
            "date": fallback_date,
            "status": (o.get("status") or "Delivered").replace("_", " ").title(),
            "total": o.get("total"),
            "items": [{"productId": i.get("product_id"), "quantity": i.get("quantity") or 1}
                      for i in (o.get("items") or [])],
            "shippingAddress": user["address"],
            "paymentMethod": user["paymentMethod"],
        })

    return {
        "products": products,
        "user": user,
        "cart": cart,
        "wishlist": [],
        "savedForLater": [],
        "orders": orders,
        "reviews": [],
        "recentSearches": [],
        "recentlyViewed": [p["id"] for p in products[:3]],
    }


def task_ids() -> dict[str, str]:
    """{M111: 'M111/false_premise_masks_expired_card'} from the built data.json."""
    f = ROOT / "data.json"
    if not f.exists():
        return {}
    return {t["mnum"]: t["task_id"] for t in json.loads(f.read_text())["tasks"]}


def check(state: dict, who: str) -> list[str]:
    """Properties the static environment must hold to not misrepresent itself."""
    problems = []
    now = datetime.datetime.now(datetime.timezone.utc)
    ids = {p.get("id") for p in state.get("products") or []}
    for o in state.get("orders") or []:
        for i in o.get("items") or []:
            if i.get("productId") not in ids:
                problems.append(f"{who}: order {o.get('id')} item {i.get('productId')} "
                                f"is not in the catalogue — renders with no name or image")
        raw = o.get("date")
        try:
            age = (now - datetime.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))).days
        except ValueError:
            problems.append(f"{who}: order {o.get('id')} has an unparseable date {raw!r}")
            continue
        if age > 90:
            problems.append(f"{who}: order {o.get('id')} is dated {str(raw)[:10]} ({age}d ago) "
                            f"— outside the Orders page's default 'past 3 months' tab, so it "
                            f"will not be rendered")
        if o.get("total") is None:
            problems.append(f"{who}: order {o.get('id')} has no total")
    for pid in {i.get("productId") for i in state.get("cart") or []}:
        if pid not in ids:
            problems.append(f"{who}: cart line {pid} is not in the catalogue")
    return problems


def export_seeds() -> tuple[int, list[str]]:
    gym, problems = _gym(), []
    ids = task_ids()
    if not gym:
        print("  falling back to the packaged payload — the static env will be degraded "
              "(filtered catalogue, no order totals, approximated dates)", file=sys.stderr)
    for task_dir in sorted(SAMPLES.iterdir()):
        if not task_dir.is_dir():
            continue
        seed_dir = task_dir / "seed_data"
        if not seed_dir.is_dir():
            continue
        mnum = task_dir.name.split("_", 1)[0]
        n = 0
        for sf in sorted(seed_dir.glob("seed_[0-9].json")):
            seed_n = sf.stem.rsplit("_", 1)[1]
            state = None
            if gym and ids.get(mnum):
                dump_world, transform_shop = gym
                try:
                    state = transform_shop(dump_world(ids[mnum], int(seed_n))["shop"])
                except Exception as exc:
                    print(f"  !! {mnum}/{seed_n} gym build failed ({exc}) — using the payload",
                          file=sys.stderr)
            if state is None:
                state = pack_to_shop(json.loads(sf.read_text()))
            out = OUT / "seeds" / mnum / seed_n
            out.mkdir(parents=True, exist_ok=True)
            (out / "shop.json").write_text(json.dumps(state, indent=2) + "\n")
            # empty companions so links are consistent; mocks fall back to defaults
            for app in ("mail", "market", "food"):
                p = out / f"{app}.json"
                if not p.exists():
                    p.write_text("{}\n")
            problems += check(state, f"{mnum}/{seed_n}")
            n += 1
        print(f"  {mnum}: {n} seed(s)")
    return n, problems


def build_mocks() -> None:
    if not HUB.is_dir():
        sys.exit(f"CUA-Gym-Hub not found at {HUB} — need the symlink for builds")
    for app, dirname in APPS.items():
        src = HUB / dirname
        if not (src / "node_modules" / ".bin" / "vite").exists():
            print(f"  skip {dirname} — npm install missing", file=sys.stderr)
            continue
        print(f"  build {dirname} → env_ui/{app}/")
        subprocess.check_call(
            ["./node_modules/.bin/vite", "build", "--base", "./"],
            cwd=src,
        )
        dest = OUT / app
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src / "dist", dest)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    print("seeds:")
    _, problems = export_seeds()
    print()
    if problems:
        print("PROBLEMS — the exported environment misrepresents itself:")
        for p in problems:
            print(f"  !! {p}")
    else:
        print("  every order is inside the default 'past 3 months' tab, has a total, and "
              "every ordered/carted product resolves in the catalogue")
    # Static JSON cannot age with the wall clock: dates are frozen at export time, so
    # roughly three months from now the orders drop off the default tab again. Say when.
    print(f"\n  exported {datetime.date.today()} — re-run before "
          f"{datetime.date.today() + datetime.timedelta(days=80)} or the orders "
          f"age out of the Orders page again")
    if os.environ.get("SEEDS_ONLY"):
        print("SEEDS_ONLY set — skipping the mock build")
        return
    print("\nmocks:")
    build_mocks()
    print("done →", OUT)


if __name__ == "__main__":
    main()
