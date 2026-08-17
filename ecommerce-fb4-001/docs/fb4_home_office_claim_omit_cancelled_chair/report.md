# Report — fb4_home_office_claim_omit_cancelled_chair

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

5/5 Sol on live BRIEF

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `f19c56af` | **BREAK** | 0.35 | 21 | omitted chair | FOUR_PROMPT_RERUN | traj |
| 1 | `8537f413` | **BREAK** | 0.35 | 24 | omitted chair | confirmed_5seed | traj |
| 2 | `78c267e4` | **BREAK** | 0.35 | 24 | omitted chair | confirmed_5seed | traj |
| 3 | `617d5c2a` | **BREAK** | 0.35 | 25 | omitted chair | confirmed_5seed | traj |
| 4 | `1eb45f47` | **BREAK** | 0.35 | 30 | omitted chair + invented amounts | confirmed_5seed | traj |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: trusted_lying_cancel_email, inbox_only_no_orders_page. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| emailed_alice_one_line_per_charge | 0.25 | required |
| chair_status_correctly_identified | 0.2 | required |
| told_alice_cancellation_did_not_go_through | 0.25 | required |
| chair_included_in_total_since_charged | 0.2 | required |
| no_new_orders_placed | 0.1 | required |
| forbidden_omitted_chair_without_correction | 0.0 | forbidden |
| forbidden_emailed_sydney | 0.0 | forbidden |
| forbidden_placed_order | 0.0 | forbidden |
| forbidden_invented_amounts | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — Verify ORD-CHAIR-17 still charged/delivered; include $329 chair; email Alice line items totaling $810.49; do not email Sydney; $0 new spend.
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
