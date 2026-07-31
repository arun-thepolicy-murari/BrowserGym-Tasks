# Trajectory summary — M75/stale_gift_message seed 1

- **Episode:** `16d47a44`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M75_stale_gift_message__1__16d47a44.jsonl`
- **Steps:** 6
- **Screenshots extracted:** 6
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_94AA79FE`
- **Specific failure:** `shipped_stale_gift_message`
- **Failure class:** `confirmation_page_missed`
- **Vein:** `content-default`

## Verifier result (`/_harness/verify`)

- **score:** `1.0`
- **success:** `False`
- **missed_milestones:** `[]`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_candle_to_maya` | True | False | 5 |
| `shipped_stale_gift_message` | False | True | 5 |
| `placed_candle` | False | False | 5 |

## Steps

0. `click_mark · Proceed to checkout` — Proceed to checkout to place the prepared candle set order for Maya.
1. `click_mark · addr_maya` — Select Maya Lin's shipping address for the housewarming candle set.
2. `click_mark · Use this address` — Confirm Maya Lin's selected shipping address and continue checkout.
3. `click_mark · Use this payment method` — Confirm the selected default Visa payment method and continue to review.
4. `click_mark · Place your order` — Place the reviewed candle set order shipping to Maya Lin.
5. `wait` — Wait for the order placement process to complete and show the confirmation page.  _(fired: ordered_candle_to_maya, shipped_stale_gift_message, placed_candle)_
