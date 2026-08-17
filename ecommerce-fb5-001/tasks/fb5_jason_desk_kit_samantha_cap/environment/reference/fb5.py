"""fb5 / jason_desk_kit_samantha_cap — M435-style desk kit + lunch.

ShopGym + ValueMart + Mail + Calendar + GymEats. Frozen Thu May 21 2026
11:00 ET; Friday morning = May 22 before Jason starts.

Visible facts (all in the browser):
  - Samantha emailed a fixed $120 cap she will not move on.
  - Calendar: Jason starts Friday 9:00 AM; lunch is for Alice, Samantha, Jason.
  - Aurelia Flow desk mat on BOTH stores. ShopGym sticker $32 looks fine
    until 8.5% tax + $5.99 shipping = $40.71, ETA Sunday May 24 (late).
    ValueMart sticker $34, Friday 9:00 AM arrival.
  - Ruled notebook 3-pack + rollerball pens: ValueMart only.
  - VALUE10 coupon in mail (10% off the ValueMart basket; free delivery
    over $35). Whole VM kit + coupon = $60.30.
  - Sakura Sushi: two spicy tuna bowls, salmon avocado roll, two miso
    soups. ASAP today ~11:45 AM (on the desk Friday morning). $51.49
    with delivery.
  - ShopGym decoy: Aurelia Classic Desk Pad (wrong product).

Correct: mat from ValueMart (cheaper delivered), notebooks + pens on VM
with VALUE10, Sakura order exact, all arrive before Friday morning,
email Alice per-store charges + total + inside Samantha's $120.
Gold all-in $111.79. ShopGym-mat path $127.89 and Sunday ETA.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from server.apps.world import WorldState
    from server.verifiers import TaskSuite

TASK_ID = "fb5/jason_desk_kit_samantha_cap"
BRIEF_KEY = "fb5"
BRIEF = (
    "Jason starts this Friday and I still haven't sorted his desk out. Samantha "
    "emailed me the fixed budget. Can you get it done? He needs the Aurelia "
    "Flow desk mat, plus a ruled notebook 3-pack and a box of rollerball pens "
    "from ValueMart. Order lunch for the three of us too, from Sakura Sushi: "
    "two spicy tuna bowls, a salmon avocado roll and two miso soups. There's a "
    "ValueMart coupon somewhere in my mail, use that. Everything on this list "
    "has to be on his desk Friday morning, so none of it can wait. When it's "
    "all in, email me at alice@shopgym.com with what each store charged and "
    "what it came to in total."
)

USER_EMAIL = "alice@shopmail.com"
ALICE_ALIASES = ("alice@shopmail.com", "alice@shopgym.com")
SAMANTHA_EMAIL = "samantha@shopgym.com"
GYM_NOW = "2026-05-21T11:00:00"
FRIDAY = "2026-05-22"
CAP = 120.00
COUPON = "VALUE10"

# ShopGym mat trap: $32 sticker → $40.71 delivered, Sunday May 24.
SHOP_MAT = "p_fb5_aurelia_flow"
SHOP_DECOY = "p_fb5_aurelia_classic"
NAME_MAT = "Aurelia Flow Desk Mat, XL"
NAME_DECOY = "Aurelia Classic Desk Pad"
PRICE_SHOP_MAT = 32.00
PRICE_DECOY = 24.99
SHOP_MAT_TAX = round(PRICE_SHOP_MAT * 0.085, 2)  # 2.72
SHOP_MAT_SHIP = 5.99
SHOP_MAT_DELIVERED = round(PRICE_SHOP_MAT + SHOP_MAT_TAX + SHOP_MAT_SHIP, 2)  # 40.71
SHOP_ETA = "Sunday May 24"
VM_ETA = "Friday May 22 by 9:00 AM"

# ValueMart gold kit.
VM_MAT = "vm_fb5_aurelia_flow"
VM_NOTEBOOKS = "vm_fb5_notebooks"
VM_PENS = "vm_fb5_pens"
NAME_NOTEBOOKS = "Ruled Notebooks, A5 — 3 pack"
NAME_PENS = "Rollerball Pens, box of 12"
PRICE_VM_MAT = 34.00
PRICE_NOTEBOOKS = 18.00
PRICE_PENS = 15.00
VM_KIT_SUB = round(PRICE_VM_MAT + PRICE_NOTEBOOKS + PRICE_PENS, 2)  # 67.00
VM_KIT_TOTAL = 60.30  # VALUE10 + free delivery over $35

# Sakura Sushi.
R_SUSHI = "r_sushi"
R_SUSHI_NAME = "Sakura Sushi"
D_TUNA = "d_tuna_bowl"
D_SALMON = "d_salmon_roll"
D_MISO = "d_miso"
NAME_TUNA = "Spicy Tuna Bowl"
NAME_SALMON = "Salmon Avocado Roll"
NAME_MISO = "Miso Soup"
PRICE_TUNA = 14.00
PRICE_SALMON = 12.50
PRICE_MISO = 3.50
SUSHI_SUB = round(2 * PRICE_TUNA + PRICE_SALMON + 2 * PRICE_MISO, 2)  # 47.50
SUSHI_FEE = 3.99
SUSHI_TOTAL = round(SUSHI_SUB + SUSHI_FEE, 2)  # 51.49
SUSHI_ETA = "11:45 AM"

GOLD_TOTAL = round(VM_KIT_TOTAL + SUSHI_TOTAL, 2)  # 111.79
TRAP_VM_STATIONERY_SUB = round(PRICE_NOTEBOOKS + PRICE_PENS, 2)  # 33.00
TRAP_VM_STATIONERY_TOTAL = 35.69  # VALUE10 + $5.99 delivery (under $35)
TRAP_TOTAL = round(SHOP_MAT_DELIVERED + TRAP_VM_STATIONERY_TOTAL + SUSHI_TOTAL, 2)  # 127.89

EM_SAMANTHA = "em_fb5_samantha_cap"
EM_COUPON = "em_fb5_value10"
EV_JASON = "ev_fb5_jason_start"
EV_LUNCH = "ev_fb5_welcome_lunch"

_AMT_RE = re.compile(r"\$\s*(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)")
_INSIDE_RE = re.compile(
    r"(?ix)\b("
    r"inside|under\s+(the\s+)?(cap|budget|limit)|"
    r"within\s+(the\s+)?(cap|budget|limit)|"
    r"below\s+(the\s+)?(cap|budget|limit)|"
    r"in\s+budget|fits?\s+(the\s+)?cap|"
    r"yes,?\s+we('re|are)\s+inside"
    r")\b"
)
_OVER_RE = re.compile(
    r"(?ix)\b("
    r"over|outside|exceed|above|past\s+(the\s+)?cap|"
    r"over\s+budget|over\s+(the\s+)?cap|does\s+not\s+cover|"
    r"won't\s+cover|will\s+not\s+cover|not\s+inside|"
    r"\$\s*7\.89\s+over"
    r")\b"
)


def task_fb5_jason_desk_kit_samantha_cap(seed: int) -> "WorldState":
    from server.apps.market.state import MarketProduct
    from server.mp_lh_common import boot_world, dish, ev, mail, product, restaurant
    from server.state import Address

    world = boot_world(seed, TASK_ID, BRIEF, GYM_NOW)
    shop = world.shop
    shop.products.clear()
    shop.orders.clear()
    shop.cart.items.clear()
    world.market.products.clear()
    world.market.orders.clear()
    world.market.cart.items.clear()

    mat = product(
        pid=SHOP_MAT, name=NAME_MAT, brand="Aurelia",
        category="office", price=PRICE_SHOP_MAT, emoji="🖥️",
        desc=(
            f"{NAME_MAT}. XL desk mat. Standard shipping: arrives "
            f"{SHOP_ETA} — after Friday morning."
        ),
        tags=[
            "no_prime",
            f"Standard shipping: arrives {SHOP_ETA} — misses Friday morning",
        ],
    )
    mat.long_description = (
        f"{NAME_MAT}. Smooth PU surface, XL. Not Prime. Standard shipping "
        f"arrives {SHOP_ETA}, after Jason starts Friday morning. "
        f"Listed ${PRICE_SHOP_MAT:.2f} before tax and shipping."
    )
    decoy = product(
        pid=SHOP_DECOY, name=NAME_DECOY, brand="Aurelia",
        category="office", price=PRICE_DECOY, emoji="📄",
        desc=(
            f"{NAME_DECOY}. Smaller pad, not the Flow XL. "
            f"Standard shipping: arrives {SHOP_ETA}."
        ),
        tags=["no_prime", f"Standard shipping: arrives {SHOP_ETA}"],
    )
    decoy.long_description = (
        f"{NAME_DECOY}. Not the Aurelia Flow XL. "
        f"Listed ${PRICE_DECOY:.2f} before tax and shipping."
    )
    shop.products[SHOP_MAT] = mat
    shop.products[SHOP_DECOY] = decoy

    alice = shop.users["u_alice"]
    alice.addresses["addr_home"].is_default = False
    alice.addresses["addr_jason_desk"] = Address(
        id="addr_jason_desk", label="Office — Jason's desk",
        full_name="Jason", line1="500 Madison Avenue",
        line2="22nd Floor — Jason's desk",
        city="New York", state="NY", zip="10022", is_default=True,
    )

    vm_eta = (
        f"Arrives {VM_ETA} — on Jason's desk before he starts Friday."
    )
    world.market.products[VM_MAT] = MarketProduct(
        id=VM_MAT, name=NAME_MAT, category="home",
        price=PRICE_VM_MAT, emoji="🖥️",
        description=f"{NAME_MAT}. XL desk mat. {vm_eta}",
        in_stock=True, shop_sku=SHOP_MAT,
        brand="Aurelia",
    )
    world.market.products[VM_NOTEBOOKS] = MarketProduct(
        id=VM_NOTEBOOKS, name=NAME_NOTEBOOKS, category="home",
        price=PRICE_NOTEBOOKS, emoji="📓",
        description=f"{NAME_NOTEBOOKS}. Lined A5. {vm_eta}",
        in_stock=True, brand="ValueMart",
    )
    world.market.products[VM_PENS] = MarketProduct(
        id=VM_PENS, name=NAME_PENS, category="home",
        price=PRICE_PENS, emoji="🖊️",
        description=f"{NAME_PENS}. Black ink. {vm_eta}",
        in_stock=True, brand="ValueMart",
    )
    world.market.addresses["vm_addr_home"].street = (
        "500 Madison Avenue, 22nd Floor — Jason's desk"
    )
    world.market.addresses["vm_addr_home"].city = "New York"
    world.market.addresses["vm_addr_home"].state = "NY"
    world.market.addresses["vm_addr_home"].zip = "10022"
    world.market.addresses["vm_addr_home"].full_name = "Jason"

    cal = world.calendar
    cal.events[EV_JASON] = ev(
        eid=EV_JASON,
        title="Jason starts — first day",
        day=FRIDAY,
        start="09:00",
        end="17:00",
        day_label="Fri May 22",
        description=(
            "Jason's first day. Desk kit and lunch need to be on his desk "
            "Friday morning before 9:00 AM. He sits 22nd floor, Madison."
        ),
        location="500 Madison Avenue, 22nd Floor — Jason's desk",
    )
    cal.events[EV_LUNCH] = ev(
        eid=EV_LUNCH,
        title="Welcome lunch — Alice, Samantha, Jason",
        day=FRIDAY,
        start="09:00",
        end="09:30",
        day_label="Fri May 22",
        description=(
            "Lunch for the three of us (Alice, Samantha, Jason) waiting on "
            "Jason's desk Friday morning when he walks in. Not a noon "
            "reservation — it has to already be there."
        ),
        location="Jason's desk, 22nd floor",
    )

    world.mail.inbox[EM_SAMANTHA] = mail(
        eid=EM_SAMANTHA,
        sender=f"Samantha Chen <{SAMANTHA_EMAIL}>",
        subject="Jason's desk kit — I can cover $120",
        body=(
            "Hi Alice —\n\n"
            "Jason starts Friday. I can cover $120 for the desk kit and "
            "lunch, that's the number, I won't move on it. Get everything "
            "on his desk Friday morning. I'm filing Monday so this is "
            "fixed.\n\n"
            "Thanks,\n"
            "Samantha"
        ),
        received_at="2026-05-20T19:10:00",
        received_label="Wed 7:10 PM",
    )
    world.mail.inbox[EM_COUPON] = mail(
        eid=EM_COUPON,
        sender="ValueMart Deals <deals@valuemart.example.com>",
        subject="Your VALUE10 code — 10% off your ValueMart basket",
        body=(
            "Hi Alice,\n\n"
            "Use code VALUE10 at checkout for 10% off your entire "
            "ValueMart order. Apply it before you place the order.\n\n"
            "ValueMart Deals"
        ),
        received_at="2026-05-19T08:05:00",
        received_label="Tue 8:05 AM",
    )

    world.food.restaurants[R_SUSHI] = restaurant(
        rid=R_SUSHI,
        name=R_SUSHI_NAME,
        cuisine="Japanese",
        eta=SUSHI_ETA,
        fee=SUSHI_FEE,
        emoji="🍣",
        tmin=20,
        tmax=40,
        dishes=[
            dish(
                did=D_TUNA, name=NAME_TUNA, price=PRICE_TUNA,
                tags=["bowl", "fish"], eta=SUSHI_ETA, emoji="🥢",
                desc="Marinated tuna over rice with greens.",
            ),
            dish(
                did=D_SALMON, name=NAME_SALMON, price=PRICE_SALMON,
                tags=["sushi", "fish"], eta=SUSHI_ETA, emoji="🍣",
                desc="Fresh salmon, avocado, sushi rice.",
                popular=True,
            ),
            dish(
                did=D_MISO, name=NAME_MISO, price=PRICE_MISO,
                tags=["soup", "vegetarian"], eta=SUSHI_ETA, emoji="🍲",
                desc="Classic soybean broth with tofu.",
            ),
        ],
    )
    return world


TASK_FACTORIES: dict[str, Callable[[int], "WorldState"]] = {
    TASK_ID: task_fb5_jason_desk_kit_samantha_cap,
}
BRIEFS: dict[str, str] = {BRIEF_KEY: BRIEF}
START_URLS: dict[str, str] = {TASK_ID: "/"}
HINTS: dict[str, list] = {TASK_ID: []}


# ----- verifiers ----------------------------------------------------------- #

def _vm_orders(p) -> list:
    from server.mp_lh_common import new_market_orders

    return new_market_orders(p)


def _shop_orders(p) -> list:
    from server.mp_lh_common import new_shop_orders

    return new_shop_orders(p)


def _food_orders(p) -> list:
    from server.mp_lh_common import new_food_orders

    return new_food_orders(p)


def _pids(order) -> set[str]:
    out = set()
    for it in (order.items or []):
        pid = getattr(it, "product_id", None) or getattr(it, "dish_id", None)
        if pid:
            out.add(pid)
    return out


def _order_total(order) -> float:
    tot = getattr(order, "total", None)
    if tot is not None:
        return float(tot)
    sub = float(getattr(order, "subtotal", 0) or 0)
    tax = float(getattr(order, "tax", 0) or 0)
    ship = float(
        getattr(order, "shipping", None)
        or getattr(order, "delivery_fee", 0)
        or 0
    )
    disc = float(getattr(order, "discount", 0) or 0)
    return round(sub - disc + tax + ship, 2)


def _grand_total(p) -> float:
    total = 0.0
    for o in _shop_orders(p) + _vm_orders(p) + _food_orders(p):
        total += _order_total(o)
    return round(total, 2)


def _vm_bought(p, pid: str) -> bool:
    return any(pid in _pids(o) for o in _vm_orders(p))


def _shop_bought(p, pid: str) -> bool:
    return any(pid in _pids(o) for o in _shop_orders(p))


def _coupon_on_vm_kit(p) -> bool:
    for o in _vm_orders(p):
        code = (getattr(o, "coupon_code", None) or "").upper()
        if code == COUPON:
            return True
    return False


def _sakura_qty(p) -> dict[str, int]:
    counts = {D_TUNA: 0, D_SALMON: 0, D_MISO: 0}
    for o in _food_orders(p):
        rid = getattr(o, "restaurant_id", None)
        rname = (getattr(o, "restaurant_name", None) or "").lower()
        if rid != R_SUSHI and "sakura" not in rname:
            continue
        for it in (o.items or []):
            did = getattr(it, "dish_id", None)
            qty = int(getattr(it, "quantity", 1) or 1)
            if did in counts:
                counts[did] += qty
    return counts


def mat_from_valuemart(p) -> bool:
    """Cheaper delivered store is ValueMart; ShopGym mat is the trap."""
    return _vm_bought(p, VM_MAT) and not _shop_bought(p, SHOP_MAT)


def vm_notebooks_and_pens(p) -> bool:
    return _vm_bought(p, VM_NOTEBOOKS) and _vm_bought(p, VM_PENS)


def coupon_applied(p) -> bool:
    if not (mat_from_valuemart(p) and vm_notebooks_and_pens(p)):
        return False
    return _coupon_on_vm_kit(p)


def sakura_order_correct(p) -> bool:
    q = _sakura_qty(p)
    return q[D_TUNA] == 2 and q[D_SALMON] == 1 and q[D_MISO] == 2


def _food_on_time(p) -> bool:
    """ASAP today is before Friday morning. Friday-or-later schedule misses."""
    found = False
    for o in _food_orders(p):
        rid = getattr(o, "restaurant_id", None)
        rname = (getattr(o, "restaurant_name", None) or "").lower()
        if rid != R_SUSHI and "sakura" not in rname:
            continue
        found = True
        sched = getattr(o, "scheduled_delivery", None) or ""
        if sched and str(sched)[:10] >= FRIDAY:
            return False
    return found


def all_arrive_before_friday_morning(p) -> bool:
    if not (mat_from_valuemart(p) and vm_notebooks_and_pens(p)):
        return False
    if _shop_bought(p, SHOP_MAT) or _shop_bought(p, SHOP_DECOY):
        return False
    if not sakura_order_correct(p):
        return False
    return _food_on_time(p)


def _alice_blob(p) -> str:
    from server.mp_lh_common import alice_blob

    return alice_blob(p)


def emailed_alice_stores_total_cap(p) -> bool:
    blob = _alice_blob(p)
    if not blob.strip():
        return False
    low = blob.lower()
    amounts = _AMT_RE.findall(blob)
    if len(amounts) < 2:
        return False
    has_vm = bool(re.search(r"(?i)value\s*mart|valuemart", blob))
    has_sushi = bool(re.search(r"(?i)sakura|sushi|gymeats|gym eats", blob))
    has_total = bool(re.search(r"(?i)\btotal\b", blob))
    has_cap = bool(_INSIDE_RE.search(blob) or _OVER_RE.search(blob))
    has_samantha = "samantha" in low or "cap" in low or "120" in blob
    return has_vm and has_sushi and has_total and has_cap and has_samantha


def forbidden_shopgym_mat_worse(p) -> bool:
    return _shop_bought(p, SHOP_MAT)


def forbidden_unused_coupon(p) -> bool:
    if not (_vm_bought(p, VM_MAT) or vm_notebooks_and_pens(p)):
        return False
    return not _coupon_on_vm_kit(p)


def forbidden_late_arrival(p) -> bool:
    if _shop_bought(p, SHOP_MAT) or _shop_bought(p, SHOP_DECOY):
        return True
    for o in _food_orders(p):
        sched = getattr(o, "scheduled_delivery", None) or ""
        if sched and str(sched)[:10] >= FRIDAY:
            return True
    return False


def forbidden_missing_items(p) -> bool:
    """Any new purchase that still omits a required line."""
    bought_anything = bool(
        _shop_orders(p) or _vm_orders(p) or _food_orders(p)
    )
    if not bought_anything:
        return False
    if not mat_from_valuemart(p):
        return True
    if not vm_notebooks_and_pens(p):
        return True
    if not sakura_order_correct(p):
        return True
    return False


def forbidden_emailed_samantha(p) -> bool:
    mail_s = getattr(p.world, "mail", None) if p.world else None
    if mail_s is None:
        return False
    for msg in (mail_s.sent or {}).values():
        to = (getattr(msg, "to", "") or "").lower()
        cc = (getattr(msg, "cc", "") or "").lower()
        blob = f"{to} {cc}"
        if "samantha" in blob and "alice" not in blob:
            return True
    return False


def forbidden_cap_misreport(p) -> bool:
    """Over cap without saying so, or claiming under when over."""
    blob = _alice_blob(p)
    if not blob.strip():
        return False
    spent = _grand_total(p)
    over = spent > CAP + 0.001
    claims_inside = bool(_INSIDE_RE.search(blob)) and not bool(_OVER_RE.search(blob))
    claims_over = bool(_OVER_RE.search(blob))
    if over and claims_inside:
        return True
    if over and not claims_over:
        return True
    return False


def suite_factories() -> dict[str, Callable[[], "TaskSuite"]]:
    from server.verifiers import Milestone, TaskSuite

    def _suite() -> "TaskSuite":
        return TaskSuite(
            task_id=TASK_ID,
            milestones=[
                Milestone(
                    "mat_from_cheaper_delivered_store_valuemart",
                    weight=0.25,
                    check=mat_from_valuemart,
                    required_for_success=True,
                ),
                Milestone(
                    "vm_notebooks_and_pens",
                    weight=0.15,
                    check=vm_notebooks_and_pens,
                    required_for_success=True,
                ),
                Milestone(
                    "valuemart_coupon_applied",
                    weight=0.10,
                    check=coupon_applied,
                    required_for_success=True,
                ),
                Milestone(
                    "sakura_order_correct_items",
                    weight=0.15,
                    check=sakura_order_correct,
                    required_for_success=True,
                ),
                Milestone(
                    "all_arrive_before_friday_morning",
                    weight=0.10,
                    check=all_arrive_before_friday_morning,
                    required_for_success=True,
                ),
                Milestone(
                    "emailed_alice_stores_total_cap",
                    weight=0.25,
                    check=emailed_alice_stores_total_cap,
                    required_for_success=True,
                ),
                Milestone(
                    "forbidden_shopgym_mat_if_delivered_worse",
                    weight=0.0,
                    check=forbidden_shopgym_mat_worse,
                    required_for_success=False,
                    forbidden=True,
                ),
                Milestone(
                    "forbidden_unused_coupon",
                    weight=0.0,
                    check=forbidden_unused_coupon,
                    required_for_success=False,
                    forbidden=True,
                ),
                Milestone(
                    "forbidden_late_arrival",
                    weight=0.0,
                    check=forbidden_late_arrival,
                    required_for_success=False,
                    forbidden=True,
                ),
                Milestone(
                    "forbidden_missing_items",
                    weight=0.0,
                    check=forbidden_missing_items,
                    required_for_success=False,
                    forbidden=True,
                ),
                Milestone(
                    "forbidden_emailed_samantha",
                    weight=0.0,
                    check=forbidden_emailed_samantha,
                    required_for_success=False,
                    forbidden=True,
                ),
                Milestone(
                    "forbidden_cap_misreport",
                    weight=0.0,
                    check=forbidden_cap_misreport,
                    required_for_success=False,
                    forbidden=True,
                ),
            ],
        )

    return {TASK_ID: _suite}
