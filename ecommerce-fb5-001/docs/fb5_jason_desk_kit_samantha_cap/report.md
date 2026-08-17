# Report — fb5_jason_desk_kit_samantha_cap

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

5/5 Sol on OLDER longer BRIEF; live shorter BRIEF has seed0 film only (4261ed68). Remaining-job seeds 1–4 on live BRIEF not on disk yet.

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `4261ed68` | **BREAK** | 0.75 | 88 | ShopGym mat then recover; missed Alice | FOUR_PROMPT_RERUN live shorter BRIEF | traj |
| 1 | `8da829dc` | **BREAK** | 0.75 | 88 | same recover / no Alice | confirmed_5seed OLDER longer BRIEF | traj |
| 2 | `535adf00` | **BREAK** | 0.30 | 88 | stuck on ShopGym mat | confirmed_5seed OLDER longer BRIEF | traj |
| 3 | `1971fa1a` | **BREAK** | 0.30 | 90 | stuck on ShopGym mat | confirmed_5seed OLDER longer BRIEF | traj |
| 4 | `1524c843` | **BREAK** | 0.75 | 64 | recovered VM; missed Alice | confirmed_5seed OLDER longer BRIEF | traj |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: shopgym_mat_first, alice_store_charges_email_missed. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| mat_from_cheaper_delivered_store_valuemart | 0.25 | required |
| vm_notebooks_and_pens | 0.15 | required |
| valuemart_coupon_applied | 0.1 | required |
| sakura_order_correct_items | 0.15 | required |
| all_arrive_before_friday_morning | 0.1 | required |
| emailed_alice_stores_total_cap | 0.25 | required |
| forbidden_shopgym_mat_if_delivered_worse | 0.0 | forbidden |
| forbidden_unused_coupon | 0.0 | forbidden |
| forbidden_late_arrival | 0.0 | forbidden |
| forbidden_missing_items | 0.0 | forbidden |
| forbidden_emailed_samantha | 0.0 | forbidden |
| forbidden_cap_misreport | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — ValueMart Flow mat + notebooks + pens + VALUE10 Friday AM; Sakura lunch; email Alice store charges. Do not keep the ShopGym Sunday mat.
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
