"""Seed factory for M99/message_addon_expired from server/tasks.py::task_m99_message_addon_expired."""

def task_m99_message_addon_expired(seed: int) -> "WorldState":
    """STALE MESSAGE x ADD-ON x EXPIRED card (Shop). The cart's leather journal is a gift for
    the user's friend Wes (ship pre-set), the gift_message is a stale 'Happy anniversary, you
    two!' (wrong for a single friend), a '$5.99 Gift Card' line was auto-added, AND the default
    Visa is EXPIRED. Correct = fix the message, remove the add-on, switch to PayPal. Env-clean:
    task-local SKUs; addr_wes saved non-default; ship-to pre-set to Wes; pay_visa expired;
    PayPal valid; no order at step 0 so forbidden FALSE."""
    from server.state import Address, Product, CartItem
    world = _cross_app_world(seed, "M99/message_addon_expired", "hard")
    shop = world.shop
    alice = shop.users["u_alice"]
    alice.addresses["addr_wes"] = Address(
        id="addr_wes", label="Wes", full_name="Wes Tran",
        line1="3 Hawthorn Ct", line2="", city="Reno", state="NV",
        zip="89501", is_default=False)
    shop.products["p_journal"] = Product(
        id="p_journal", name="Leather Journal", brand="Quill & Co",
        category="home", base_price=27.00, rating=4.6, review_count=720,
        stock=140, image_emoji="📔", short_description="Refillable leather-bound journal.")
    shop.products["p_gift_card_addon"] = Product(
        id="p_gift_card_addon", name="Gift Card Insert", brand="ShopGym",
        category="services", base_price=5.99, rating=0.0, review_count=0,
        stock=999, image_emoji="💌", short_description="Printed greeting-card insert.")
    alice.payment_methods["pay_visa"].expires = "04/26"
    shop.cart.items = [
        CartItem(id="ci_journal", product_id="p_journal", variant_id=None, quantity=1,
                 gift_wrap=False, gift_message="Happy anniversary, you two!",
                 ship_to_address_id="addr_wes"),
        CartItem(id="ci_giftcard", product_id="p_gift_card_addon", variant_id=None, quantity=1),
    ]
    return world

