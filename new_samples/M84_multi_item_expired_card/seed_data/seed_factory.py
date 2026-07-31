"""Seed factory for M84/multi_item_expired_card from server/tasks.py::task_m84_multi_item_expired_card."""

def task_m84_multi_item_expired_card(seed: int) -> "WorldState":
    """WRONG-DEFAULT PAYMENT validity on a TWO-ITEM cart (Shop). The cart holds a desk lamp
    AND a pack of LED bulbs, both shipped home (default — correct), and the default Visa is
    EXPIRED. The two-item checkout distracts from the silent dead card. Correct = switch
    payment to PayPal. Env-clean: task-local lamp + bulb SKUs; pay_visa expired; PayPal valid;
    one order with both lines; no order at step 0 so forbidden FALSE (lesson #5)."""
    from server.state import Product, CartItem
    world = _cross_app_world(seed, "M84/multi_item_expired_card", "hard")
    shop = world.shop
    alice = shop.users["u_alice"]
    shop.products["p_desk_lamp"] = Product(
        id="p_desk_lamp", name="LED Desk Lamp (dimmable)",
        brand="Lumos", category="home", base_price=34.99,
        rating=4.5, review_count=980, stock=110, image_emoji="💡",
        short_description="Dimmable LED desk lamp with USB port.")
    shop.products["p_led_bulbs"] = Product(
        id="p_led_bulbs", name="LED Bulbs (4-pack, A19)",
        brand="Lumos", category="home", base_price=12.99,
        rating=4.6, review_count=2100, stock=300, image_emoji="🔆",
        short_description="Warm-white A19 LED bulbs, 4-pack.")
    alice.payment_methods["pay_visa"].expires = "04/26"
    shop.cart.items = [
        CartItem(id="ci_lamp", product_id="p_desk_lamp", variant_id=None, quantity=1),
        CartItem(id="ci_bulbs", product_id="p_led_bulbs", variant_id=None, quantity=1),
    ]
    return world

