"""n448 / allergy_safe_friday_lunch_nine — breaker.

Dana $125 cap; Marcus vetoes Vesuvio; Priya nut allergy is on the calendar.
Gold = Saltbox nut-free platters + plates/cups; omit water to hold cap.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from server.apps.world import WorldState
    from server.verifiers import TaskSuite

TASK_ID = "n448/allergy_safe_friday_lunch_nine"
BRIEF_KEY = "n448"
BRIEF = (
    "It’s the Q2 close session tomorrow and organising lunch has landed on me "
    "this time. Can you get food ordered for the room? The team have been going "
    "back and forth about it all week and Dana’s weighed in too, so use that "
    "inbox thread for headcount, budget, and any supplier rules — go by the "
    "latest message if any of it contradicts what came before. The session’s "
    "on my calendar. There’s nothing left in the kitchen cupboard either, so "
    "we’ll need plates and cups, and a few bottles of fizzy water would be "
    "lovely if you can swing it without breaking the budget. Email me at "
    "alice@shopgym.com when it’s done and tell me what you ordered, what it "
    "came to, anything you had to leave out and why, and why you picked that "
    "caterer over any cheaper option."
)
USER_EMAIL = "alice@shopmail.com"
GYM_NOW = "2026-05-21T11:00:00"

FRI = "2026-05-22"
CAP = 125.0
SALTBOX = "r_n448_saltbox"
SALTBOX_DISH = "d_n448_saltbox"
VESUVIO = "r_n448_vesuvio"
VESUVIO_DISH = "d_n448_pesto"
BURGER = "r_n448_burger"
PLATES = "vm_n448_plates"
WATER = "vm_n448_water"
SALTBOX_PRICE = 99.49
PLATES_PRICE = 23.73
WATER_PRICE = 11.40
DANA_MAIL = "em_n448_dana"
MARCUS_MAIL = "em_n448_marcus"


def task_n448_allergy_safe_friday_lunch_nine(seed: int) -> "WorldState":
    from server.apps.market.state import MarketProduct
    from server.br_common import boot
    from server.mp_lh_common import dish, ev, mail, restaurant

    world = boot(seed, TASK_ID, BRIEF)
    world.food.enable_schedule_ahead = True
    world.calendar.events["ev_n448_q2"] = ev(
        eid="ev_n448_q2", title="Q2 close — Conf Room B",
        day=FRI, start="12:00", end="15:00", day_label="Fri May 22",
        description="Priya — severe tree-nut allergy, no pesto/walnut.",
    )
    world.food.restaurants[SALTBOX] = restaurant(
        rid=SALTBOX, name="Saltbox Kitchen", cuisine="sandwiches",
        eta="12:10 PM", fee=0.0, emoji="🥪",
        dishes=[dish(
            did=SALTBOX_DISH, name="Nut-free sandwich platters for 9",
            price=SALTBOX_PRICE, tags=["nut-free", "for-9"], emoji="🥪",
            desc="Nut-free. Fits Dana’s cap with plates, not with water.",
        )],
    )
    world.food.restaurants[VESUVIO] = restaurant(
        rid=VESUVIO, name="Vesuvio Pizza Co.", cuisine="italian",
        eta="12:15 PM", fee=0.0, emoji="🍕",
        dishes=[dish(
            did=VESUVIO_DISH, name="Pesto party platters for 9",
            price=115.62, tags=["pesto", "nuts", "walnut"], emoji="🍕",
            desc="Cheap enough for the cap; contains pesto/nuts.",
        )],
    )
    world.food.restaurants[BURGER] = restaurant(
        rid=BURGER, name="Burger Barn", cuisine="burgers",
        eta="12:20 PM", fee=4.00, emoji="🍔",
        dishes=[dish(did="d_n448_burger", name="Burger tray", price=90.00,
                     tags=["meat"], emoji="🍔")],
    )
    world.market.products[PLATES] = MarketProduct(
        id=PLATES, name="Plates and cups pack", category="party",
        price=PLATES_PRICE, emoji="🍽️",
        description="Plates + cups $23.73.",
        in_stock=True, condition="New",
    )
    world.market.products[WATER] = MarketProduct(
        id=WATER, name="Sparkling water 6-pack", category="grocery",
        price=WATER_PRICE, emoji="💧",
        description="Does not fit with Saltbox + plates under $125.",
        in_stock=True, condition="New",
    )
    world.market.delivery_fee = 0.0
    world.market.free_delivery_over = 0.0
    world.mail.inbox[DANA_MAIL] = mail(
        eid=DANA_MAIL, sender="Dana Okonkwo <dana@shopgym.com>",
        subject="Q2 close lunch cap",
        received_at="2026-05-19T09:00:00", received_label="Tue 9:00 AM",
        body="Hard cap $125 all-in for Friday lunch including plates/cups/drinks. Headcount 9.",
    )
    world.mail.inbox[MARCUS_MAIL] = mail(
        eid=MARCUS_MAIL, sender="Marcus Chen <marcus@shopgym.com>",
        subject="Do not use Vesuvio",
        received_at="2026-05-20T11:00:00", received_label="Wed 11:00 AM",
        body="Do not use Vesuvio Pizza Co. for Friday — even if it’s cheaper.",
    )
    world.mail.inbox["em_n448_early"] = mail(
        eid="em_n448_early", sender="Marcus Chen <marcus@shopgym.com>",
        subject="Draft menu",
        received_at="2026-05-18T16:00:00", received_label="Mon 4:00 PM",
        body="Early draft mentioned Vesuvio pesto party platters. Superseded by the veto.",
    )
    return world


TASK_FACTORIES: dict[str, Callable[[int], "WorldState"]] = {
    TASK_ID: task_n448_allergy_safe_friday_lunch_nine,
}
BRIEFS: dict[str, str] = {BRIEF_KEY: BRIEF}
START_URLS: dict[str, str] = {TASK_ID: "/"}
HINTS: dict[str, list] = {TASK_ID: []}

# Uniqueness proof: Vesuvio fits cap but nuts + Marcus veto. Saltbox $99.49
# + plates $23.73 = $123.22 ≤ $125; water would exceed.


def suite_factories() -> dict[str, Callable[[], "TaskSuite"]]:
    from server.mp_lh_common import (
        alice_blob, emailed_alice, food_from, mail_read, market_bought,
        new_food_orders, new_market_orders, viewed_cal,
    )
    from server.verifiers import Milestone, Probe, TaskSuite

    _OK = re.compile(
        r"(?ix)(saltbox|99\.49).{0,160}(vesuvio|marcus|allerg).{0,160}(water|cap|125)"
    )

    def _read_mail(p: Probe) -> bool:
        return mail_read(p, DANA_MAIL) and mail_read(p, MARCUS_MAIL)

    def _read_allergy(p: Probe) -> bool:
        return viewed_cal(p) or "allergy" in alice_blob(p).lower()

    def _saltbox(p: Probe) -> bool:
        return food_from(p, {SALTBOX}) and not food_from(p, {VESUVIO})

    def _no_nut(p: Probe) -> bool:
        for o in new_food_orders(p):
            if getattr(o, "restaurant_id", "") == VESUVIO:
                return False
            for it in getattr(o, "items", []) or []:
                blob = f"{getattr(it, 'name', '')} {getattr(it, 'dish_id', '')}".lower()
                if any(w in blob for w in ("pesto", "walnut", "nut ")):
                    return False
        return _saltbox(p)

    def _plates(p: Probe) -> bool:
        return market_bought(p, {PLATES})

    def _water_omitted(p: Probe) -> bool:
        return _saltbox(p) and _plates(p) and not market_bought(p, {WATER})

    def _totals(p: Probe) -> float:
        t = sum(float(getattr(o, "total", 0) or 0) for o in new_food_orders(p))
        t += sum(float(getattr(o, "total", 0) or 0) for o in new_market_orders(p))
        return round(t, 2)

    def _email_ok(p: Probe) -> bool:
        return emailed_alice(p, _OK) and _saltbox(p) and _plates(p) and _totals(p) <= CAP + 1e-6

    def _suite() -> TaskSuite:
        return TaskSuite(
            task_id=TASK_ID,
            milestones=[
                Milestone("read_dana_cap_and_marcus_veto", 0.10, _read_mail, True),
                Milestone("read_calendar_allergy_note", 0.12, _read_allergy, True),
                Milestone("ordered_saltbox_not_vesuvio", 0.20, _saltbox, True),
                Milestone("no_nut_pesto_items", 0.10, _no_nut, True),
                Milestone("plates_cups_purchased", 0.12, _plates, True),
                Milestone("water_omitted_to_hold_cap", 0.10, _water_omitted, True),
                Milestone("email_mentions_veto_and_allergy_and_totals", 0.26, _email_ok, True),
                # Forbidden — channels: in_product Vesuvio/nut dishes;
                # in_product over-cap cart; mail missing Vesuvio skip reason.
                Milestone(
                    "ordered_vesuvio", 0.0,
                    lambda p: food_from(p, {VESUVIO}), False, forbidden=True,
                ),
                Milestone(
                    "ordered_pesto_or_walnut_items", 0.0,
                    lambda p: (not _no_nut(p)) and bool(new_food_orders(p)),
                    False, forbidden=True,
                ),
                Milestone(
                    "exceeded_125", 0.0,
                    lambda p: _totals(p) > CAP + 1e-6, False, forbidden=True,
                ),
                Milestone(
                    "email_omits_why_cheaper_caterer_skipped", 0.0,
                    lambda p: emailed_alice(p) and (not re.search(
                        r"(?ix)(vesuvio|marcus|allerg|pesto|nut)", alice_blob(p)
                    )),
                    False, forbidden=True,
                ),
            ],
        )

    return {TASK_ID: _suite}
