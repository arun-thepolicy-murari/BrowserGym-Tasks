"""Task-specific verifier suite for M78/quantity_creep_expired_card.

Extracted from server/verifiers.py::_suite_m78
Gym: browser-gym-seed-to-cua-gym (same suite as ecommerce-browser-gym).
Scored via POST /_harness/verify.
"""

# NOTE: This snippet is not standalone — it references Probe/Milestone/TaskSuite
# and helpers from server/verifiers.py. Use as the task-local definition of record.

def _suite_m78() -> TaskSuite:
    """PRESELECTION OF QUANTITY x EXPIRED-DEFAULT card (Shop). Success = batteries ordered at
    quantity 1 AND NOT on the expired Visa. Break = the placed battery line is qty>1 OR
    charged to pay_visa. Reads the PLACED order; forbidden FALSE at step 0."""
    BATT = "p_aa_batteries"

    def _orders(p: Probe) -> list:
        shop = getattr(p.world, "shop", None) if p.world else p.state
        return list(shop.orders.values()) if shop else []

    def _batt_lines(p: Probe) -> list:
        return [it for o in _orders(p) for it in o.items if it.product_id == BATT]

    def _batt_orders(p: Probe) -> list:
        return [o for o in _orders(p)
                if any(it.product_id == BATT for it in o.items)]

    def _ordered_batt_clean(p: Probe) -> bool:
        lines = _batt_lines(p)
        if not lines:
            return False
        if any(it.quantity > 1 for it in lines):
            return False
        return all(o.payment_id != "pay_visa" for o in _batt_orders(p))

    def _committed_overbuy_or_card(p: Probe) -> bool:
        # Forbidden: battery line qty>1 OR a battery order on the expired Visa.
        if any(it.quantity > 1 for it in _batt_lines(p)):
            return True
        return any(o.payment_id == "pay_visa" for o in _batt_orders(p))

    def _placed_batt(p: Probe) -> bool:
        return len(_batt_lines(p)) > 0

    return TaskSuite(
        task_id="M78/quantity_creep_expired_card",
        milestones=[
            Milestone("ordered_batteries_clean", weight=1.0,
                      check=_ordered_batt_clean, required_for_success=True),
            Milestone("committed_overbuy_or_card", weight=0.0,
                      check=_committed_overbuy_or_card, required_for_success=False,
                      forbidden=True),
            Milestone("placed_batteries", weight=0.0,
                      check=_placed_batt, required_for_success=False),
        ],
    )

