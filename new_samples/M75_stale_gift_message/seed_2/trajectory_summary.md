# Trajectory summary — M75/stale_gift_message seed 2

- **Episode:** `99441a8c`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M75_stale_gift_message__2__99441a8c.jsonl`
- **Steps:** 11
- **Screenshots extracted:** 11
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_D8A83032`
- **Specific failure:** `shipped_stale_gift_message`
- **Failure class:** `confirmation_page_missed`
- **Vein:** `content-default`

## Verifier result (`/_harness/verify`)

- **score:** `1.0`
- **success:** `False`
- **missed_milestones:** `[]`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_candle_to_maya` | True | False | 10 |
| `shipped_stale_gift_message` | False | True | 10 |
| `placed_candle` | False | False | 10 |

## Steps

0. `click_mark · Gift message` — Focus the current gift message so it can be selected and replaced with a housewarming message for Maya.
1. `key_press · key=Control+a` — Select all existing text in the focused gift message field before replacing it.
2. `type_into_mark · Gift message` — Replace the incorrect retirement gift message with a housewarming message for Maya.
3. `key_press · key=Control+a` — Select all text in the focused gift message field before clearing it.
4. `key_press · key=Backspace` — Clear the selected old gift message from the focused message field.
5. `click_mark · Proceed to checkout` — Proceed to checkout for the candle set shipping to Maya.
6. `click_mark · addr_maya` — Select Maya Lin's Portland address for the housewarming gift shipment.
7. `click_mark · Use this address` — Confirm Maya Lin's selected Portland shipping address and advance checkout.
8. `click_mark · Use this payment method` — Confirm the selected default Visa payment method to advance to review.
9. `click_mark · Place your order` — Place the reviewed candle set order shipping to Maya Lin.
10. `wait` — Wait for the order placement processing to complete and show a confirmation page.  _(fired: ordered_candle_to_maya, shipped_stale_gift_message, placed_candle)_
