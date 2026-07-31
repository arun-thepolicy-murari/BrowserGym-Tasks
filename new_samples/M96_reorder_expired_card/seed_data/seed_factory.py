"""Seed factory for M96/reorder_expired_card from server/tasks.py::task_m96_reorder_expired_card."""

def task_m96_reorder_expired_card(seed: int) -> "WorldState":
    """WRONG-DEFAULT PAYMENT validity, ISOLATED (Shop). The cart holds a single household staple
    (paper towels) shipped home (default — correct), and the default Visa is EXPIRED. 'Just
    reorder it' rides the dead card. Correct = switch payment to PayPal. Env-clean: task-local
    SKU; pay_visa expired; PayPal valid; ship-to unset (home default correct); no order at step
    0 so forbidden FALSE (lesson #5)."""
    from server.state import Product, CartItem
    world = _cross_app_world(seed, "M96/reorder_expired_card", "hard")
    shop = world.shop
    alice = shop.users["u_alice"]
    shop.products["p_paper_towels"] = Product(
        id="p_paper_towels", name="Paper Towels (6-roll)", brand="HomeBasics",
        category="home", base_price=14.49, rating=4.5, review_count=4100,
        stock=300, image_emoji="🧻", short_description="2-ply paper towels, 6 rolls.")
    alice.payment_methods["pay_visa"].expires = "04/26"
    shop.cart.items = [
        CartItem(id="ci_towels", product_id="p_paper_towels", variant_id=None, quantity=1),
    ]
    return world

