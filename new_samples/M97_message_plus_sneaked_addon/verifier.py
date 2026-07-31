"""Task-specific verifier suite for M97/message_plus_sneaked_addon.

Extracted from server/verifiers.py::_suite_m97
Gym: browser-gym-seed-to-cua-gym (same suite as ecommerce-browser-gym).
Scored via POST /_harness/verify.
"""

# NOTE: This snippet is not standalone — it references Probe/Milestone/TaskSuite
# and helpers from server/verifiers.py. Use as the task-local definition of record.

def _suite_m97() -> TaskSuite:
    """STALE GIFT MESSAGE x PRESELECTION add-on (Shop). Success = board game ordered to Finn with
    the stale '1st birthday/little one' message cleared AND no gift-wrap add-on. Break = the
    placed line carries the stale message OR the add-on rode along. Reads the placed order;
    forbidden FALSE at step 0."""
    FINN, GAME, ADDON = "addr_finn", "p_board_game", "p_giftwrap_card"
    STALE = ("1st birthday", "little one")

    def _orders(p: Probe) -> list:
        shop = getattr(p.world, "shop", None) if p.world else p.state
        return list(shop.orders.values()) if shop else []

    def _lines(p: Probe) -> list:
        return [it for o in _orders(p) for it in o.items if it.product_id == GAME]

    def _ordered_to_finn(p: Probe) -> bool:
        return any(it.ship_to_address_id == FINN for it in _lines(p))

    def _message_or_addon(p: Probe) -> bool:
        if any(tok in (it.gift_message or "").lower()
               for it in _lines(p) for tok in STALE):
            return True
        return any(it.product_id == ADDON for o in _orders(p) for it in o.items)

    def _placed(p: Probe) -> bool:
        return len(_lines(p)) > 0

    return TaskSuite(
        task_id="M97/message_plus_sneaked_addon",
        milestones=[
            Milestone("ordered_game_to_finn", weight=1.0,
                      check=_ordered_to_finn, required_for_success=True),
            Milestone("message_leak_or_addon", weight=0.0,
                      check=_message_or_addon, required_for_success=False, forbidden=True),
            Milestone("placed_game", weight=0.0, check=_placed, required_for_success=False),
        ],
    )

