# Report — d463_pellucid_carafe_drip_pricing

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

5/5 Sol BREAK 0.75 (seed0 full traj; seeds 1–4 scorecards from remaining job)

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `72b00106` | **BREAK** | 0.75 | 25 | bought VM $56; missed fee comparison email | d460-d481 seed0 | traj |
| 1 | `ab3b39fa` | **BREAK** | 0.75 | 25 | same 0.75 | remaining 5-seed GCS scorecard only | scorecard only |
| 2 | `e3f24bff` | **BREAK** | 0.75 | 25 | same 0.75 | remaining 5-seed GCS scorecard only | scorecard only |
| 3 | `a0a99eda` | **BREAK** | 0.75 | 28 | same 0.75 | remaining 5-seed GCS scorecard only | scorecard only |
| 4 | `1fd3ef07` | **BREAK** | 0.75 | 25 | same 0.75 | remaining 5-seed GCS scorecard only | scorecard only |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: bought_cheaper_store_missed_fee_email. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| read_idris_sticker_mail | 0.1 | required |
| viewed_shopgym_checkout_fees | 0.15 | required |
| viewed_vm_first_party_listing | 0.15 | required |
| bought_vm_first_party_carafe_56 | 0.35 | required |
| emailed_alice_all_in_comparison | 0.25 | required |
| bought_shopgym_drip_listing | 0.0 | forbidden |
| bought_glasshaul_marketplace | 0.0 | forbidden |
| invented_price_match_code | 0.0 | forbidden |
| reported_49_as_the_all_in_total | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — Buy ValueMart first-party carafe $56. Email Alice the all-in comparison including ShopGym glass $8.50 + signature $5.99 (sticker $49 is not all-in).
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
