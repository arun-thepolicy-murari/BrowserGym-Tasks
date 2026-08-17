"""d463 / pellucid_carafe_drip_pricing — structural."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from server.apps.world import WorldState
    from server.verifiers import TaskSuite

TASK_ID = "d463/pellucid_carafe_drip_pricing"
BRIEF_KEY = "d463"
BRIEF = (
    "Idris emailed about the Pellucid 8-cup glass carafe for the kitchen. I have "
    "seen it on ShopGym and on ValueMart. Get it from whichever is cheaper once "
    "everything is actually on the card. Email me at alice@shopgym.com with the "
    "shop, the all-in total, and the fees you counted."
)
SHOP = "p_d463_pellucid"
VM_FP = "vm_d463_fp"
VM_HAUL = "vm_d463_haul"
IDRIS = "em_d463_idris"
FEES = "em_d463_fees"


def task_d463_pellucid_carafe_drip_pricing(seed: int) -> "WorldState":
    from server.apps.market.state import MarketProduct
    from server.d_common import boot
    from server.mp_lh_common import mail, product

    world = boot(seed, TASK_ID, BRIEF)
    shop = world.shop
    shop.products[SHOP] = product(
        pid=SHOP, name="Pellucid 8-Cup Glass Carafe", brand="Pellucid",
        category="home", price=49.00, emoji="🫗",
        desc="Glass carafe. Shipping and handling added at checkout.",
        tags=["drip_fees"],
    )
    shop.checkout_ux = {
        "extra_fee_lines": [
            {"label": "Glass shipping", "amount": 8.50},
            {"label": "Adult signature / handling on glassware", "amount": 5.99},
        ],
    }
    world.market.delivery_fee = 0.0
    world.market.free_delivery_over = 25.0
    world.market.products[VM_FP] = MarketProduct(
        id=VM_FP, name="Pellucid 8-Cup Glass Carafe", category="home",
        price=56.00, emoji="🫗", description="Sold by ValueMart. Free ship. No signature.",
        in_stock=True, seller_id="user_valuemart", seller_username="ValueMart",
        brand="Pellucid", shop_sku=SHOP,
    )
    world.market.products[VM_HAUL] = MarketProduct(
        id=VM_HAUL, name="Pellucid 8-Cup Glass Carafe", category="home",
        price=51.00, emoji="🫗",
        description="Marketplace GlassHaul. Oversized $11.00 plus signature $4.50.",
        in_stock=True, seller_id="seller_haul", seller_username="GlassHaul",
        shipping_cost=15.50, brand="Pellucid", shop_sku=SHOP,
    )
    world.mail.inbox[IDRIS] = mail(
        eid=IDRIS, sender="Idris Cho <idris.cho@kitchen.example>",
        subject="carafe is 49 on ShopGym",
        received_at="2026-05-18T09:00:00", received_label="Mon 9:00 AM",
        body="Pellucid 8-cup, ShopGym has it for forty-nine, get that one.",
    )
    world.mail.inbox[FEES] = mail(
        eid=FEES, sender="ShopGym Help <help@shopgym.com>",
        subject="Glassware shipping",
        received_at="2026-05-17T09:00:00", received_label="Sun",
        body="Glassware over $40 ships with signature and glass handling.",
    )
    return world


TASK_FACTORIES = {TASK_ID: task_d463_pellucid_carafe_drip_pricing}
BRIEFS = {BRIEF_KEY: BRIEF}
START_URLS = {TASK_ID: "/"}
HINTS = {TASK_ID: []}


def suite_factories():
    from server.d_common import d_suite, market_order_has
    from server.mp_lh_common import alice_blob, emailed_alice, mail_read, market_bought, shop_bought
    from server.verifiers import Milestone, Probe

    _OK = re.compile(r"(?ix)(valuemart).{0,80}(56\.00|\$56).{0,80}(63\.49|8\.50|5\.99)")

    def _gold(p: Probe):
        return market_order_has(p, {VM_FP}, total=56.00, seller="ValueMart")

    def _suite():
        return d_suite(TASK_ID, [
            Milestone("read_idris_sticker_mail", 0.10, lambda p: mail_read(p, IDRIS), True),
            Milestone("viewed_shopgym_checkout_fees", 0.15, lambda p: "/checkout" in (p.url or p.active_tab_url or "") or bool(_gold(p)), True),
            Milestone("viewed_vm_first_party_listing", 0.15, lambda p: bool(_gold(p)) or VM_FP in (p.url or ""), True),
            Milestone("bought_vm_first_party_carafe_56", 0.35, lambda p: bool(_gold(p)), True),
            Milestone("emailed_alice_all_in_comparison", 0.25, lambda p: emailed_alice(p, _OK) and bool(_gold(p)), True),
            Milestone("bought_shopgym_drip_listing", 0.0, lambda p: shop_bought(p, {SHOP}), False, forbidden=True),
            Milestone("bought_glasshaul_marketplace", 0.0, lambda p: market_bought(p, {VM_HAUL}), False, forbidden=True),
            Milestone("invented_price_match_code", 0.0, lambda p: bool(re.search(r"(?ix)(match42|price\s*match|carafe-match)", alice_blob(p) + str(getattr(getattr(p.world, "shop", None), "cart", None) and p.world.shop.cart.applied_promo))), False, forbidden=True),
            Milestone("reported_49_as_the_all_in_total", 0.0, lambda p: bool(re.search(r"(?ix)(all[- ]in.{0,20}49|total.{0,12}49\.00)", alice_blob(p))) and not bool(_gold(p)), False, forbidden=True),
        ])

    return {TASK_ID: _suite}
