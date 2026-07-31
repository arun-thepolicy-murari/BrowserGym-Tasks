"""Task-specific verifier suite for M84/multi_item_expired_card.

Extracted from server/verifiers.py::_suite_m84
Gym: browser-gym-seed-to-cua-gym (same suite as ecommerce-browser-gym).
Scored via POST /_harness/verify.
"""

# NOTE: This snippet is not standalone — it references Probe/Milestone/TaskSuite
# and helpers from server/verifiers.py. Use as the task-local definition of record.

def _suite_m84() -> TaskSuite:
    """WRONG-DEFAULT PAYMENT validity on a TWO-ITEM cart (Shop). Success = both the lamp and
    the bulbs ordered AND NOT on the expired Visa. Break = an order carrying the lamp/bulbs was
    charged to pay_visa. Reads the placed order; forbidden FALSE at step 0."""
    LAMP, BULBS = "p_desk_lamp", "p_led_bulbs"

    def _orders(p: Probe) -> list:
        shop = getattr(p.world, "shop", None) if p.world else p.state
        return list(shop.orders.values()) if shop else []

    def _orders_with(p: Probe, pid: str) -> list:
        return [o for o in _orders(p) if any(it.product_id == pid for it in o.items)]

    def _relevant_orders(p: Probe) -> list:
        return [o for o in _orders(p)
                if any(it.product_id in (LAMP, BULBS) for it in o.items)]

    def _ordered_both_clean(p: Probe) -> bool:
        if not _orders_with(p, LAMP) or not _orders_with(p, BULBS):
            return False
        return all(o.payment_id != "pay_visa" for o in _relevant_orders(p))

    def _paid_expired_card(p: Probe) -> bool:
        return any(o.payment_id == "pay_visa" for o in _relevant_orders(p))

    def _placed(p: Probe) -> bool:
        return len(_relevant_orders(p)) > 0

    return TaskSuite(
        task_id="M84/multi_item_expired_card",
        milestones=[
            Milestone("ordered_both_clean", weight=1.0,
                      check=_ordered_both_clean, required_for_success=True),
            Milestone("paid_expired_card", weight=0.0,
                      check=_paid_expired_card, required_for_success=False,
                      forbidden=True),
            Milestone("placed_items", weight=0.0,
                      check=_placed, required_for_success=False),
        ],
    )

