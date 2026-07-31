#!/usr/bin/env python3
"""Build CUA mock UIs into env_ui/ and export per-task shop seed JSON.

The packaged wave-1 seeds only carry shop state, so we transform that into the
amazon_mock shape. Built assets use Vite base './' + HashRouter so they work on
GitHub Pages and local http.server without a bridge.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HUB = ROOT / "CUA-Gym-Hub" / "websites"
OUT = ROOT / "env_ui"
SAMPLES = ROOT / "new_samples"

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

    orders = []
    for o in seed.get("orders_at_seed") or []:
        orders.append({
            "id": o.get("id"),
            "date": "2024-01-01T00:00:00.000Z",
            "status": (o.get("status") or "Delivered").title(),
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


def export_seeds() -> int:
    n = 0
    for task_dir in sorted(SAMPLES.iterdir()):
        if not task_dir.is_dir():
            continue
        seed_dir = task_dir / "seed_data"
        if not seed_dir.is_dir():
            continue
        mnum = task_dir.name.split("_", 1)[0]
        for sf in sorted(seed_dir.glob("seed_[0-9].json")):
            seed_n = sf.stem.rsplit("_", 1)[1]
            raw = json.loads(sf.read_text())
            out = OUT / "seeds" / mnum / seed_n
            out.mkdir(parents=True, exist_ok=True)
            (out / "shop.json").write_text(json.dumps(pack_to_shop(raw), indent=2) + "\n")
            # empty companions so links are consistent; mocks fall back to defaults
            for app in ("mail", "market", "food"):
                p = out / f"{app}.json"
                if not p.exists():
                    p.write_text("{}\n")
            n += 1
            print(f"  seed {mnum}/{seed_n}")
    return n


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
    n = export_seeds()
    print(f"  {n} seed files")
    print("mocks:")
    build_mocks()
    print("done →", OUT)


if __name__ == "__main__":
    main()
