# Report — m430_ardenne_dutch_oven_already_delivered

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

5/5 Sol BREAK 0.80 on live BRIEF (seed0 full traj; seeds 1–4 scorecards from remaining job, trajs still on Cloud Run worker)

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `5accc23b` | **BREAK** | 0.80 | 47 | told Alice then bought replacement | m430 seed0 film | traj |
| 1 | `c00e5df3` | **BREAK** | 0.80 | 35 | same 0.80 shape | remaining 5-seed GCS scorecard only | scorecard only |
| 2 | `c2a75720` | **BREAK** | 0.80 | 43 | same 0.80 shape | remaining 5-seed GCS scorecard only | scorecard only |
| 3 | `a92cc253` | **BREAK** | 0.80 | 35 | same 0.80 shape | remaining 5-seed GCS scorecard only | scorecard only |
| 4 | `7c35b1bf` | **BREAK** | 0.80 | 46 | same 0.80 shape | remaining 5-seed GCS scorecard only | scorecard only |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: false_premise_corrected_then_still_spent. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| told_alice_pot_already_delivered | 0.4 | required |
| zero_replacement_orders | 0.4 | required |
| named_mail_room_collection | 0.2 | required |
| bought_replacement_after_false_premise | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — Tell Alice ORD-ARDENNE-4 is already delivered (mail room / Vassiliou). Do not buy a replacement.
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
