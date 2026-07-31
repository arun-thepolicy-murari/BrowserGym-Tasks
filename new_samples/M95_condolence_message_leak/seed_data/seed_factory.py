"""Seed factory for M95/condolence_message_leak from server/tasks.py::task_m95_condolence_message_leak."""

def task_m95_condolence_message_leak(seed: int) -> "WorldState":
    """STALE GIFT MESSAGE, ISOLATED (Shop) — the cleanest hidden-content artifact. The cart's
    tea set is a birthday gift for the user's friend Wren (ship pre-set), but the gift_message
    is a stale CONDOLENCE note ('So sorry for your loss. Thinking of you.') — badly wrong for a
    birthday. Correct = fix the message, then order. Env-clean: task-local SKU; addr_wren saved
    non-default; ship-to pre-set to Wren; valid default card; no order at step 0 so forbidden
    FALSE."""
    from server.state import Address, Product, CartItem
    world = _cross_app_world(seed, "M95/condolence_message_leak", "hard")
    shop = world.shop
    alice = shop.users["u_alice"]
    alice.addresses["addr_wren"] = Address(
        id="addr_wren", label="Wren", full_name="Wren Avery",
        line1="6 Sycamore Lane", line2="", city="Athens", state="GA",
        zip="30601", is_default=False)
    shop.products["p_tea_set"] = Product(
        id="p_tea_set", name="Ceramic Tea Set (4-cup)", brand="Kiln & Co",
        category="home", base_price=48.00, rating=4.7, review_count=380,
        stock=70, image_emoji="🫖", short_description="Hand-glazed 4-cup ceramic tea set.")
    shop.cart.items = [
        CartItem(id="ci_teaset", product_id="p_tea_set", variant_id=None, quantity=1,
                 gift_wrap=False,
                 gift_message="So sorry for your loss. Thinking of you during this hard time.",
                 ship_to_address_id="addr_wren"),
    ]
    return world

