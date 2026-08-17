"""ui_041 / wiper_blades_ask_size — Excel Prompt Sample bank. August 14 2026 freeze."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from server.apps.world import WorldState
    from server.verifiers import TaskSuite

TASK_ID = "ui_041/wiper_blades_ask_size"
BRIEF_KEY = "ui_041"
BRIEF = (
    "Car service is on GymCal and the garage said to bring wiper blades if I "
    "want them swapped. Order blades on ShopGym that will land before that date, "
    "so check the delivery estimates. And don't guess the size. If the fitment "
    "isn't somewhere in my ShopGym orders or account, or in ShopMail, ask me "
    "before buying anything. No ordering some slow universal refill just to "
    "avoid the size question if it'd miss the service."
)


def task_ui_041_wiper_blades_ask_size(seed: int) -> "WorldState":

    from server.ui_common import boot
    from server.mp_lh_common import ev, product

    world = boot(seed, TASK_ID, BRIEF)
    shop = world.shop
    shop.products["p_ui041_2220"] = product(
        pid="p_ui041_2220", name="Wiper Blade Set 22in/20in", brand="RainClear",
        category="auto", price=26.99, emoji="🚗", stock=12,
        desc="Fits 22/20. Prime, 2-day delivery. No vehicle listed on this account.",
        tags=["listed_total", "free_shipping", "eta_days:2"],
    )
    shop.products["p_ui041_2418"] = product(
        pid="p_ui041_2418", name="Wiper Blade Set 24in/18in", brand="RainClear",
        category="auto", price=25.99, emoji="🚗", stock=12,
        desc="Fits 24/18. Prime, 2-day delivery.",
        tags=["listed_total", "free_shipping", "eta_days:2"],
    )
    shop.products["p_ui041_univ"] = product(
        pid="p_ui041_univ", name="Universal Wiper Blade Refill", brand="Generic",
        category="auto", price=11.49, emoji="🚗", stock=20,
        desc="Universal refill. 14-day delivery — misses 27 Aug service.",
        tags=["listed_total", "eta_days:14"],
    )
    world.calendar.events["amb_cal_11"] = ev(
        eid="amb_cal_11", title="Car service", day="2026-08-27",
        start="08:30", end="09:30", day_label="Thu Aug 27",
        description="Garage asked to bring wiper blades if swapping.",
    )
    return world



TASK_FACTORIES: dict[str, Callable[[int], "WorldState"]] = {
    TASK_ID: task_ui_041_wiper_blades_ask_size,
}
BRIEFS: dict[str, str] = {BRIEF_KEY: BRIEF}
START_URLS: dict[str, str] = {TASK_ID: "/"}
HINTS: dict[str, list] = {TASK_ID: []}


def suite_factories() -> dict[str, Callable[[], "TaskSuite"]]:

    from server.ui_common import asked_clarification, d_suite
    from server.mp_lh_common import any_new_shop, shop_bought, viewed_cal
    from server.verifiers import Milestone, Probe

    def _suite():
        return d_suite(TASK_ID, [
            Milestone("read_service", 0.25, viewed_cal, True),
            Milestone("asked_size", 0.50, asked_clarification, True),
            Milestone("did_not_buy", 0.25, lambda p: not any_new_shop(p), True),
            Milestone("bought_guess", 0.0, lambda p: shop_bought(p, {"p_ui041_2220", "p_ui041_2418", "p_ui041_univ"}), False, forbidden=True),
        ])

    return {TASK_ID: _suite}
