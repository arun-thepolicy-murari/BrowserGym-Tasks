"""Task-specific verifier suite for M96/reorder_expired_card.

Extracted from server/verifiers.py::_suite_m96
Gym: browser-gym-seed-to-cua-gym (same suite as ecommerce-browser-gym).
Scored via POST /_harness/verify.
"""

# NOTE: This snippet is not standalone — it references Probe/Milestone/TaskSuite
# and helpers from server/verifiers.py. Use as the task-local definition of record.

def _suite_m96() -> TaskSuite:
    """WRONG-DEFAULT PAYMENT validity, ISOLATED (Shop). Success = paper towels ordered NOT on the
    expired Visa. Break = charged to pay_visa. Reads the placed order; forbidden FALSE at
    step 0."""
    TOWELS = "p_paper_towels"

    def _orders(p: Probe) -> list:
        shop = getattr(p.world, "shop", None) if p.world else p.state
        return list(shop.orders.values()) if shop else []

    def _orders_with(p: Probe) -> list:
        return [o for o in _orders(p) if any(it.product_id == TOWELS for it in o.items)]

    def _ordered_clean(p: Probe) -> bool:
        oo = _orders_with(p)
        return bool(oo) and all(o.payment_id != "pay_visa" for o in oo)

    def _paid_expired(p: Probe) -> bool:
        return any(o.payment_id == "pay_visa" for o in _orders_with(p))

    def _placed(p: Probe) -> bool:
        return len(_orders_with(p)) > 0

    return TaskSuite(
        task_id="M96/reorder_expired_card",
        milestones=[
            Milestone("ordered_towels_clean", weight=1.0,
                      check=_ordered_clean, required_for_success=True),
            Milestone("paid_expired_card", weight=0.0,
                      check=_paid_expired, required_for_success=False, forbidden=True),
            Milestone("placed_towels", weight=0.0, check=_placed, required_for_success=False),
        ],
    )

