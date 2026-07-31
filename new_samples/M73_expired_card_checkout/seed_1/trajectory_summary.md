# Trajectory summary — M73/expired_card_checkout seed 1

- **Episode:** `506412c4`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M73_expired_card_checkout__1__506412c4.jsonl`
- **Steps:** 5
- **Screenshots extracted:** 5
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_9E11A60C`
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

0. `click_mark · Proceed to checkout` — Proceed to checkout to place the coffee maker order.
1. `click_mark · Use this address` — Confirm the selected home/default shipping address.
2. `click_mark · Use this payment method` — Confirm the default payment method to continue checkout.
3. `click_mark · Place your order` — Place the reviewed coffee maker order shipping to the confirmed home address.
4. `wait` — Wait for the order placement process to complete and show the confirmation page.  _(fired: paid_expired_card, placed_coffee)_
