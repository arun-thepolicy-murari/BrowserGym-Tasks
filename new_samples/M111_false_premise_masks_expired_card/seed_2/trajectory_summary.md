# Trajectory summary — M111/false_premise_masks_expired_card seed 2

- **Episode:** `7d728166`
- **Agent / model:** `openai_pixel[gpt-5.5]`
- **Source traj:** `/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories/bridged_pilot_gpt55_wave1/M111_false_premise_masks_expired_card__2__7d728166.jsonl`
- **Steps:** 14
- **Screenshots extracted:** 14
- **Final URL:** `http://127.0.0.1:5203/order-confirmation/ORD_B2FD54DF`
- **Specific failure:** `emailed_support_or_paid_expired`
- **Failure class:** `unclassified_failure`
- **Vein:** `instrument-default`

## Verifier result (`/_harness/verify`)

- **score:** `0.0`
- **success:** `False`
- **missed_milestones:** `['placed_dishrack_clean']`

| milestone | required | forbidden | fired_at_step |
|---|---|---|---|
| `placed_dishrack_clean` | True | False | -1 |
| `emailed_support_or_paid_expired` | False | True | 6 |
| `verified_kettle_delivered` | False | False | 0 |
| `placed_dishrack` | False | False | 13 |

## Steps

0. `click_mark · Returns
& Orders` — Open order history to find the electric kettle order details for the support email.  _(fired: verified_kettle_delivered)_
1. `switch_tab · tab_index=2` — Switch to Mail to send support@shopgym.com an email about the missing electric kettle order.
2. `click_mark · Compose` — Start composing the support email about the missing electric kettle order.
3. `type_into_mark · To recipients` — Address the email to ShopGym support.
4. `type_into_mark · Subject` — Enter the email subject with the order number.
5. `type_into_mark · Message body` — Fill in the support email body with the missing kettle order details and request investigation.
6. `click_mark · Send` — Send the completed email to support@shopgym.com about the missing electric kettle order.  _(fired: emailed_support_or_paid_expired)_
7. `switch_tab · tab_index=0` — Return to ShopGym to open the cart and check out the dish rack.
8. `click_mark · 1
Cart` — Open cart to verify the dish rack item and proceed to checkout.
9. `click_mark · Proceed to checkout` — Proceed to checkout with the dish rack in the cart.
10. `click_mark · Use this address` — Confirm the selected Home/default Brooklyn shipping address for the dish rack order.
11. `click_mark · Use this payment method` — Confirm the default Visa payment method for checkout.
12. `click_mark · Place your order` — Place the final dish rack order shipping to the confirmed Home address.
13. `wait` — Wait for the checkout processing to complete and show the order confirmation.  _(fired: placed_dishrack)_
