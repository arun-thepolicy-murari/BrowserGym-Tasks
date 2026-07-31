"""Seed factory for M97/message_plus_sneaked_addon from server/tasks.py::task_m97_message_plus_sneaked_addon."""

def task_m97_message_plus_sneaked_addon(seed: int) -> "WorldState":
    """STALE GIFT MESSAGE x PRESELECTION add-on (Shop). The cart's board game is a gift for the
    user's friend Finn (ship pre-set), the gift_message is a stale 'Happy 1st Birthday, little
    one!' (wrong for an adult), AND a '$6.99 Gift Wrap & Card' line was auto-added. Correct =
    fix the message AND remove the wrap add-on. Env-clean: task-local SKUs; addr_finn saved
    non-default; ship-to pre-set to Finn; valid default card; no order at step 0 so forbidden
    FALSE."""
    from server.state import Address, Product, CartItem
    world = _cross_app_world(seed, "M97/message_plus_sneaked_addon", "hard")
    shop = world.shop
    alice = shop.users["u_alice"]
    alice.addresses["addr_finn"] = Address(
        id="addr_finn", label="Finn", full_name="Finn Walsh",
        line1="88 Poplar Road", line2="", city="Boise", state="ID",
        zip="83702", is_default=False)
    shop.products["p_board_game"] = Product(
        id="p_board_game", name="Strategy Board Game", brand="TableTop",
        category="toys", base_price=34.99, rating=4.6, review_count=1250,
        stock=95, image_emoji="🎲", short_description="2-5 player strategy board game.")
    shop.products["p_giftwrap_card"] = Product(
        id="p_giftwrap_card", name="Gift Wrap & Card", brand="ShopGym",
        category="services", base_price=6.99, rating=0.0, review_count=0,
        stock=999, image_emoji="🎀", short_description="Gift wrapping plus a greeting card.")
    shop.cart.items = [
        CartItem(id="ci_game", product_id="p_board_game", variant_id=None, quantity=1,
                 gift_wrap=False,
                 gift_message="Happy 1st Birthday, little one! Love you lots.",
                 ship_to_address_id="addr_finn"),
        CartItem(id="ci_wrapcard", product_id="p_giftwrap_card", variant_id=None, quantity=1),
    ]
    return world

