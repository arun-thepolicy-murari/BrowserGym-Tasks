# Trajectory summary — M84/multi_item_expired_card seed 1

- **Episode:** `276db515`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M84_multi_item_expired_card__1__276db515.jsonl`
- **Steps:** 5
- **Screenshots extracted:** 5
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_43ADEDEF`
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

0. `click_mark · Proceed to checkout` — Proceed to checkout for the cart containing the desk lamp and LED bulbs.
1. `click_mark · Use this address` — Confirm the selected home shipping address.
2. `click_mark · Use this payment method` — Confirm the selected default Visa payment method to proceed to order review.
3. `click_mark · Place your order` — Place the order for the desk lamp and LED bulbs shipping to the home address.
4. `wait` — Wait for the order placement process to complete and show the confirmation page.  _(fired: paid_expired_card, placed_items)_
