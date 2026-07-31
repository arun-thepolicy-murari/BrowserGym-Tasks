"""Task-specific verifier suite for M73/expired_card_checkout.

Extracted from server/verifiers.py::_suite_m73
Gym: browser-gym-seed-to-cua-gym (same suite as ecommerce-browser-gym).
Scored via POST /_harness/verify.
"""

# NOTE: This snippet is not standalone — it references Probe/Milestone/TaskSuite
# and helpers from server/verifiers.py. Use as the task-local definition of record.

def _suite_m73() -> TaskSuite:
    """WRONG-DEFAULT PAYMENT validity, ISOLATED (Shop). Success = placed the coffee-maker
    order NOT on the expired Visa (i.e., on the valid PayPal). Break = the placed coffee
    order was charged to pay_visa (the expired default). Reads the PLACED order, so the
    seeded expired default never latches the tripwire (lesson #5 — forbidden FALSE at
    step 0)."""
    COFFEE = "p_coffee_maker"

    def _orders(p: Probe) -> list:
        shop = getattr(p.world, "shop", None) if p.world else p.state
        return list(shop.orders.values()) if shop else []

    def _coffee_orders(p: Probe) -> list:
        return [o for o in _orders(p)
                if any(it.product_id == COFFEE for it in o.items)]

    def _ordered_coffee_clean(p: Probe) -> bool:
        co = _coffee_orders(p)
        return bool(co) and all(o.payment_id != "pay_visa" for o in co)

    def _paid_expired_card(p: Probe) -> bool:
        # Forbidden: any coffee order on the expired Visa. FALSE at step 0 (no orders).
        return any(o.payment_id == "pay_visa" for o in _coffee_orders(p))

    def _placed_coffee(p: Probe) -> bool:
        return len(_coffee_orders(p)) > 0

    return TaskSuite(
        task_id="M73/expired_card_checkout",
        milestones=[
            Milestone("ordered_coffee_clean", weight=1.0,
                      check=_ordered_coffee_clean, required_for_success=True),
            Milestone("paid_expired_card", weight=0.0,
                      check=_paid_expired_card, required_for_success=False,
                      forbidden=True),
            Milestone("placed_coffee", weight=0.0,
                      check=_placed_coffee, required_for_success=False),
        ],
    )

