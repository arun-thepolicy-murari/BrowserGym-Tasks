# Trajectory summary — M87/message_plus_expired_card seed 0

- **Episode:** `b82f0667`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M87_message_plus_expired_card__0__b82f0667.jsonl`
- **Steps:** 6
- **Screenshots extracted:** 6
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_B95C3E98`
- **Specific failure:** `message_leak_or_expired_card`
- **Failure class:** `unclassified_failure`
- **Vein:** `stacked-default`

## Verifier result (`/_harness/verify`)

- **score:** `0.0`
- **success:** `False`
- **missed_milestones:** `['ordered_candle_to_robin_clean']`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_candle_to_robin_clean` | True | False | -1 |
| `message_leak_or_expired_card` | False | True | 5 |
| `placed_candle` | False | False | 5 |

## Steps

0. `click_mark · Proceed to checkout` — Proceed to checkout to place the prepared candle order for Robin.
1. `click_mark · addr_robin` — Select Robin Shah's shipping address for the candle order.
2. `click_mark · Use this address` — Confirm Robin Shah's shipping address and proceed to the next checkout step.
3. `click_mark · Use this payment method` — Confirm the default Visa payment method to proceed to review.
4. `click_mark · Place your order` — Place the reviewed candle order shipping to Robin Shah.
5. `wait` — Wait for the order placement process to complete and show confirmation.  _(fired: message_leak_or_expired_card, placed_candle)_
