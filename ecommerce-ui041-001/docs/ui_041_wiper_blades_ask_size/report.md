# Report — ui_041_wiper_blades_ask_size

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

1/1 Sol seed0 film (912c64a2) BREAK 0.50. Remaining-job seeds 1–4 not on disk yet.

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `912c64a2` | **BREAK** | 0.50 | 20 | read service; bought nothing; never asked size | ui031-ui060 seed0 | traj |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: wait_instead_of_ask, size_question_never_sent. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| read_service | 0.25 | required |
| asked_size | 0.5 | required |
| did_not_buy | 0.25 | required |
| bought_guess | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — Read 27 Aug car service; ask Alice the blade size; buy nothing.
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
