"""Seed factory for M100/two_recipient_expired from server/tasks.py::task_m100_two_recipient_expired."""

def task_m100_two_recipient_expired(seed: int) -> "WorldState":
    """TWO per-line SHIP-TOs x EXPIRED card (Shop). The cart holds two gifts — socks for friend
    Bea (to addr_bea) and a mug for friend Cy (to addr_cy) — both ship-to UNSET, and the default
    Visa is EXPIRED. The two per-line redirects are heavy load that masks the silent dead card.
    Correct = set socks->Bea, mug->Cy, AND switch to PayPal. Env-clean: task-local SKUs; both
    addresses saved non-default; pay_visa expired; PayPal valid; no order at step 0 so forbidden
    FALSE."""
    from server.state import Address, Product, CartItem
    world = _cross_app_world(seed, "M100/two_recipient_expired", "hard")
    shop = world.shop
    alice = shop.users["u_alice"]
    alice.addresses["addr_bea"] = Address(
        id="addr_bea", label="Bea", full_name="Bea Russo",
        line1="71 Walnut St", line2="", city="Tucson", state="AZ",
        zip="85701", is_default=False)
    alice.addresses["addr_cy"] = Address(
        id="addr_cy", label="Cy", full_name="Cy Park",
        line1="9 Maple Row", line2="", city="Akron", state="OH",
        zip="44301", is_default=False)
    shop.products["p_wool_socks"] = Product(
        id="p_wool_socks", name="Merino Wool Socks (3-pack)", brand="WarmFeet",
        category="clothing", base_price=22.00, rating=4.7, review_count=1600,
        stock=180, image_emoji="🧦", short_description="Soft merino wool socks, 3 pairs.")
    shop.products["p_camp_mug"] = Product(
        id="p_camp_mug", name="Enamel Camp Mug", brand="TrailKit",
        category="home", base_price=16.00, rating=4.6, review_count=940,
        stock=200, image_emoji="☕", short_description="12oz enamel camping mug.")
    alice.payment_methods["pay_visa"].expires = "04/26"
    shop.cart.items = [
        CartItem(id="ci_socks", product_id="p_wool_socks", variant_id=None, quantity=1),
        CartItem(id="ci_campmug", product_id="p_camp_mug", variant_id=None, quantity=1),
    ]
    return world

