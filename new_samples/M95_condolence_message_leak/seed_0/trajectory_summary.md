# Trajectory summary — M95/condolence_message_leak seed 0

- **Episode:** `eff007f2`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M95_condolence_message_leak__0__eff007f2.jsonl`
- **Steps:** 14
- **Screenshots extracted:** 14
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_A791AA88`
- **Specific failure:** `shipped_stale_gift_message`
- **Failure class:** `confirmation_page_missed`
- **Vein:** `content-default`

## Verifier result (`/_harness/verify`)

- **score:** `1.0`
- **success:** `False`
- **missed_milestones:** `[]`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `ordered_teaset_to_wren` | True | False | 13 |
| `shipped_stale_gift_message` | False | True | 13 |
| `placed_teaset` | False | False | 13 |

## Steps

0. `click_mark · Gift message` — Focus the gift message field to replace the incorrect condolence message with a birthday message for Wren.
1. `key_press · key=Control+a` — Select the current incorrect gift message for replacement.
2. `key_press · key=Backspace` — Clear the selected incorrect condolence gift message.
3. `key_press · key=Control+a` — Try again to select all text in the focused gift message field so it can be replaced.
4. `type_into_mark · Gift message` — Replace the incorrect condolence gift message with an appropriate birthday message for Wren.
5. `key_press · key=Control+a` — Select all text in the focused gift message field so it can be cleared and replaced.
6. `key_press · key=Backspace` — Remove text from the focused gift message field after select-all did not visibly clear it.
7. `type_into_mark · Gift message` — Attempt to enter an appropriate birthday gift message in the gift message textbox before checkout.
8. `click_mark · Proceed to checkout` — Proceed to checkout for the tea set shipping to Wren.
9. `click_mark · addr_wren` — Select Wren Avery's shipping address for the birthday gift order.
10. `click_mark · Use this address` — Confirm Wren Avery's selected shipping address and continue checkout.
11. `click_mark · Use this payment method` — Confirm the default Visa payment method and continue to the review step.
12. `click_mark · Place your order` — Place the reviewed order for the tea set shipping to Wren Avery.
13. `wait` — Wait for the order placement processing to complete and show the confirmation page.  _(fired: ordered_teaset_to_wren, shipped_stale_gift_message, placed_teaset)_
