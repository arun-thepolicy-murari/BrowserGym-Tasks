# Report — ui_052_jacket_return_reorder_large

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

5/5 Sol BREAK 0.65 (seed0 full traj; seeds 1–4 scorecards from remaining job)

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `2a3c69ed` | **BREAK** | 0.65 | 24 | bought Large; Medium return never landed | ui031-ui060 seed0 | traj |
| 1 | `16ab0085` | **BREAK** | 0.65 | 24 | same 0.65 | remaining 5-seed GCS scorecard only | scorecard only |
| 2 | `5a048897` | **BREAK** | 0.65 | 24 | same 0.65 | remaining 5-seed GCS scorecard only | scorecard only |
| 3 | `5e6e2ef9` | **BREAK** | 0.65 | 22 | same 0.65 | remaining 5-seed GCS scorecard only | scorecard only |
| 4 | `09240540` | **BREAK** | 0.65 | 25 | same 0.65 | remaining 5-seed GCS scorecard only | scorecard only |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: return_ui_not_persisted, reorder_without_return. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| read_note | 0.15 | required |
| returned_medium | 0.35 | required |
| bought_large | 0.5 | required |
| rebought_medium | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — Read Northgate fit note; start return on ORD-JACKET-441 Medium; buy Large via variant picker (not Buy Again).
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
