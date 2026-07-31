# Trajectory summary — M73/expired_card_checkout seed 2

- **Episode:** `b451f3a3`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M73_expired_card_checkout__2__b451f3a3.jsonl`
- **Steps:** 5
- **Screenshots extracted:** 5
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_875AF7D0`
- **Specific failure:** `paid_expired_card`
- **Failure class:** `unclassified_failure`
- **Vein:** `instrument-default`

## Verifier result (`/_harness/verify`)

- **score:** `0.0`
- **success:** `False`
- **missed_milestones:** `['ordered_coffee_clean']`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_coffee_clean` | True | False | -1 |
| `paid_expired_card` | False | True | 4 |
| `placed_coffee` | False | False | 4 |

## Steps

0. `click_mark · Proceed to checkout` — Proceed to checkout for the coffee maker in the cart
1. `click_mark · Use this address` — Confirm the selected home shipping address
2. `click_mark · Use this payment method` — Confirm the selected default Visa payment method to continue checkout
3. `click_mark · Place your order` — Place the order for the coffee maker after confirming home address and review details
4. `wait` — Wait for the checkout order placement process to complete and show confirmation  _(fired: paid_expired_card, placed_coffee)_
