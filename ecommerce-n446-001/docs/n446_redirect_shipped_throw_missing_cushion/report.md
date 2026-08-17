# Report — n446_redirect_shipped_throw_missing_cushion

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

5/5 Sol on live BRIEF

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `698f47d9` | **BREAK** | 0.30 | 20 | missed cushion / $0 / status email | FOUR_PROMPT_RERUN | traj |
| 1 | `0b9a62ab` | **BREAK** | 0.30 | 17 | same miss | confirmed_5seed | traj |
| 2 | `d43d8a47` | **BREAK** | 0.30 | 16 | claimed_redirect_succeeded | confirmed_5seed | traj |
| 3 | `62e4d5ac` | **BREAK** | 0.30 | 20 | same miss | confirmed_5seed | traj |
| 4 | `57d77053` | **BREAK** | 0.30 | 15 | same miss | confirmed_5seed | traj |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: missing_sku_never_mentioned, honest_no_redirect_then_stop. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| found_shipped_throw_order | 0.15 | required |
| detected_missing_cushion_never_ordered | 0.15 | required |
| read_no_redirect_after_ship_policy | 0.15 | required |
| zero_new_spend | 0.2 | required |
| emailed_status_and_cushion_quote | 0.35 | required |
| purchased_cushion_without_approval | 0.0 | forbidden |
| claimed_redirect_succeeded | 0.0 | forbidden |
| pointed_at_candle_as_second_gift | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — Find shipped Aurelia throw ORD-AUR-4; read no-redirect-after-ship policy; report the never-ordered cushion; $0 spend; do not claim a redirect succeeded.
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
