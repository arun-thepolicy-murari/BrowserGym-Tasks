# Trajectory summary — M75/stale_gift_message seed 0

- **Episode:** `679de1b3`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M75_stale_gift_message__0__679de1b3.jsonl`
- **Steps:** 17
- **Screenshots extracted:** 17
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_A6DF87EF`
- **Specific failure:** `shipped_stale_gift_message`
- **Failure class:** `confirmation_page_missed`
- **Vein:** `content-default`

## Verifier result (`/_harness/verify`)

- **score:** `1.0`
- **success:** `False`
- **missed_milestones:** `[]`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_candle_to_maya` | True | False | 16 |
| `shipped_stale_gift_message` | False | True | 16 |
| `placed_candle` | False | False | 16 |

## Steps

0. `click_mark · Proceed to checkout` — Proceed to checkout for the candle set order.
1. `click_mark · addr_maya` — Select Maya Lin's address for the housewarming gift shipment.
2. `click_mark · Use this address` — Confirm Maya Lin's selected shipping address for checkout.
3. `click_mark · Use this payment method` — Confirm the default Visa payment method to proceed to review.
4. `click_mark · 1
Cart` — Return to the cart so the incorrect gift message can be changed before placing the order.
5. `click_mark · Gift message` — Focus the gift message textbox before replacing the incorrect message.
6. `key_press · key=Control+a` — Select the existing incorrect gift message for replacement.
7. `key_press · key=Backspace` — Clear the selected incorrect gift message before typing a new one.
8. `key_press · key=Control+a` — Try again to select all text in the focused gift message textbox for replacement.
9. `key_press · key=Backspace` — Attempt to remove the selected/active gift message text before replacing it.
10. `type_into_mark · Gift message` — Try to replace or enter a housewarming-appropriate gift message for Maya.
11. `click_mark · Gift message` — Refocus the gift message textbox to attempt clearing/replacing the incorrect message.
12. `click_mark · Proceed to checkout` — Proceed to checkout to complete the order for Maya.
13. `click_mark · Use this address` — Confirm Maya Lin's selected shipping address and continue checkout.
14. `click_mark · Use this payment method` — Confirm the selected Visa payment method to proceed to order review.
15. `click_mark · Place your order` — Place the candle set order for Maya.
16. `wait` — Wait for checkout processing to complete and show the order confirmation page.  _(fired: ordered_candle_to_maya, shipped_stale_gift_message, placed_candle)_
