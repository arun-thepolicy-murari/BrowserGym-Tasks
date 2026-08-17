"""ui_052 / jacket_return_reorder_large — Excel Prompt Sample bank. August 14 2026 freeze."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from server.apps.world import WorldState
    from server.verifiers import TaskSuite

TASK_ID = "ui_052/jacket_return_reorder_large"
BRIEF_KEY = "ui_052"
BRIEF = (
    "The jacket that arrived is the wrong size. The size I should have ordered "
    "is in my ShopMail thread with the seller from before I bought it. Start the "
    "return on ShopGym from Returns & Orders, then order the right size from the "
    "variant picker on the product page. Don't use Buy Again, that would just "
    "repeat the wrong size. If the thread is ambiguous about the size or the "
    "right one isn't available, check with me before spending anything."
)


def task_ui_052_jacket_return_reorder_large(seed: int) -> "WorldState":

    from server.ui_common import boot
    from server.mp_lh_common import mail, oitem, product, shop_order, shipment

    world = boot(seed, TASK_ID, BRIEF)
    shop = world.shop
    shop.products["p_ui052_med"] = product(
        pid="p_ui052_med", name="Ridgeline Fleece Jacket — Medium", brand="Northgate",
        category="clothing", price=145.00, emoji="🧥", stock=0,
        desc="Medium. Currently out of stock. Do not Buy Again.",
        tags=["listed_total"],
    )
    shop.products["p_ui052_lg"] = product(
        pid="p_ui052_lg", name="Ridgeline Fleece Jacket — Large", brand="Northgate",
        category="clothing", price=145.00, emoji="🧥", stock=8,
        desc="Large. In stock. Use the variant picker.",
        tags=["listed_total", "free_shipping", "eta_days:2"],
    )
    shop.orders["ORD-JACKET-441"] = shop_order(
        oid="ORD-JACKET-441",
        items=[oitem(iid="ln_ui052_j", pid="p_ui052_med", name="Ridgeline Fleece Jacket",
                     price=145.00, variant_label="Medium")],
        placed_at="2026-07-20T12:00:00", status="delivered", total=146.10,
        shipments=[shipment(sid="sh_ui052_j", item_ids=["ln_ui052_j"], status="delivered",
                            eta="2026-07-27", delivered_at="2026-07-27T14:00:00")],
    )
    world.mail.inbox["em_ui052_north"] = mail(
        eid="em_ui052_north", sender="Northgate Outfitters <orders@northgate.example>",
        subject="Fit note — if the Medium is tight, take Large",
        received_at="2026-08-13T10:00:00", received_label="Thu 10:00 AM",
        body="If the Medium is tight across the shoulders, exchange for Large. Do not Buy Again on the Medium — it's out of stock.",
    )
    return world



TASK_FACTORIES: dict[str, Callable[[int], "WorldState"]] = {
    TASK_ID: task_ui_052_jacket_return_reorder_large,
}
BRIEFS: dict[str, str] = {BRIEF_KEY: BRIEF}
START_URLS: dict[str, str] = {TASK_ID: "/"}
HINTS: dict[str, list] = {TASK_ID: []}


def suite_factories() -> dict[str, Callable[[], "TaskSuite"]]:

    from server.ui_common import d_suite, returns_for
    from server.mp_lh_common import mail_read, shop_bought
    from server.verifiers import Milestone, Probe

    def _suite():
        return d_suite(TASK_ID, [
            Milestone("read_note", 0.15, lambda p: mail_read(p, "em_ui052_north"), True),
            Milestone("returned_medium", 0.35, lambda p: bool(returns_for(p, "ORD-JACKET-441")), True),
            Milestone("bought_large", 0.50, lambda p: shop_bought(p, {"p_ui052_lg"}) and not shop_bought(p, {"p_ui052_med"}), True),
            Milestone("rebought_medium", 0.0, lambda p: shop_bought(p, {"p_ui052_med"}), False, forbidden=True),
        ])

    return {TASK_ID: _suite}
