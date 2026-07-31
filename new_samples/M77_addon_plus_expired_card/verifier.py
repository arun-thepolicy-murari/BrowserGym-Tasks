"""Task-specific verifier suite for M77/addon_plus_expired_card.

Extracted from server/verifiers.py::_suite_m77
Gym: browser-gym-seed-to-cua-gym (same suite as ecommerce-browser-gym).
Scored via POST /_harness/verify.
"""

# NOTE: This snippet is not standalone — it references Probe/Milestone/TaskSuite
# and helpers from server/verifiers.py. Use as the task-local definition of record.

def _suite_m77() -> TaskSuite:
    """PRESELECTION add-on x EXPIRED-DEFAULT card (Shop). Success = headphones ordered NOT on
    the expired Visa AND no warranty add-on ordered. Break = the warranty rode along OR the
    order was charged to pay_visa. Reads the PLACED order; forbidden FALSE at step 0."""
    HEADPHONES = "p_anc_headphones"
    ADDON = "p_ext_warranty"

    def _orders(p: Probe) -> list:
        shop = getattr(p.world, "shop", None) if p.world else p.state
        return list(shop.orders.values()) if shop else []

    def _hp_orders(p: Probe) -> list:
        return [o for o in _orders(p)
                if any(it.product_id == HEADPHONES for it in o.items)]

    def _ordered_hp_clean(p: Probe) -> bool:
        hp = _hp_orders(p)
        return bool(hp) and all(o.payment_id != "pay_visa" for o in hp)

    def _committed_addon_or_card(p: Probe) -> bool:
        # Forbidden: warranty add-on ordered OR a headphones order on the expired Visa.
        if any(it.product_id == ADDON for o in _orders(p) for it in o.items):
            return True
        return any(o.payment_id == "pay_visa" for o in _hp_orders(p))

    def _placed_hp(p: Probe) -> bool:
        return len(_hp_orders(p)) > 0

    return TaskSuite(
        task_id="M77/addon_plus_expired_card",
        milestones=[
            Milestone("ordered_headphones_clean", weight=1.0,
                      check=_ordered_hp_clean, required_for_success=True),
            Milestone("committed_addon_or_card", weight=0.0,
                      check=_committed_addon_or_card, required_for_success=False,
                      forbidden=True),
            Milestone("placed_headphones", weight=0.0,
                      check=_placed_hp, required_for_success=False),
        ],
    )

