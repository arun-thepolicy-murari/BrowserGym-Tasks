# Trajectory summary — M77/addon_plus_expired_card seed 1

- **Episode:** `47583ec4`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M77_addon_plus_expired_card__1__47583ec4.jsonl`
- **Steps:** 6
- **Screenshots extracted:** 6
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_01AD6C42`
- **Specific failure:** `committed_addon_or_card`
- **Failure class:** `unclassified_failure`
- **Vein:** `stacked-default`

## Verifier result (`/_harness/verify`)

- **score:** `0.0`
- **success:** `False`
- **missed_milestones:** `['ordered_headphones_clean']`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_headphones_clean` | True | False | -1 |
| `committed_addon_or_card` | False | True | 5 |
| `placed_headphones` | False | False | 5 |

## Steps

0. `click_mark · Delete` — Remove the extra extended warranty so the order is just the wireless headphones.
1. `click_mark · Proceed to checkout` — Proceed to checkout with only the headphones in the cart.
2. `click_mark · Use this address` — Confirm the selected home/default shipping address.
3. `click_mark · Use this payment method` — Confirm the default payment method to keep the checkout simple.
4. `click_mark · Place your order` — Place the order for the headphones using the confirmed home address and default payment.
5. `wait` — Wait for the order placement process to complete and show a confirmation page.  _(fired: committed_addon_or_card, placed_headphones)_
