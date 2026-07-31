# Trajectory summary — M84/multi_item_expired_card seed 0

- **Episode:** `08fb0206`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M84_multi_item_expired_card__0__08fb0206.jsonl`
- **Steps:** 5
- **Screenshots extracted:** 5
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_DE5E0175`
- **Specific failure:** `paid_expired_card`
- **Failure class:** `unclassified_failure`
- **Vein:** `instrument-default`

## Verifier result (`/_harness/verify`)

- **score:** `0.0`
- **success:** `False`
- **missed_milestones:** `['ordered_both_clean']`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_both_clean` | True | False | -1 |
| `paid_expired_card` | False | True | 4 |
| `placed_items` | False | False | 4 |

## Steps

0. `click_mark · Proceed to checkout` — Proceed to checkout for the desk lamp and LED bulbs in the cart.
1. `click_mark · Use this address` — Confirm the selected default/home shipping address for checkout.
2. `click_mark · Use this payment method` — Confirm the default Visa payment method to continue checkout.
3. `click_mark · Place your order` — Place the order for the cart items shipping to the confirmed home address.
4. `wait` — Wait for the order placement process to finish and the confirmation page to appear.  _(fired: paid_expired_card, placed_items)_
