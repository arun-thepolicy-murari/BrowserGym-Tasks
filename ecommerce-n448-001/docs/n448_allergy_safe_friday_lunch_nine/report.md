# Report — n448_allergy_safe_friday_lunch_nine

## Contextual information
See README.md and context_info.md.

## Seed table (honest coverage)

5/5 Sol on live BRIEF

| Seed | Episode | Disp | Score | Steps | Fail | Source | Artifact |
|---:|---|---|---:|---:|---|---|---|
| 0 | `155270ee` | **BREAK** | 0.52 | 47 | plates in notes not VM SKU | n440-n449 rewrite | traj |
| 1 | `5606a7f7` | **BREAK** | 0.52 | 40 | same | n448 seeds 1-4 | traj |
| 2 | `d39a7571` | **BREAK** | 0.22 | 87 | never ordered Saltbox | n448 seeds 1-4 | traj |
| 3 | `d6dabfb0` | **BREAK** | 0.52 | 72 | same as seed0 | n448 seeds 1-4 | traj |
| 4 | `39c31ae9` | **BREAK** | 0.52 | 65 | same as seed0 | n448 seeds 1-4 | traj |

Pass@n (resolve) = **0**. Frontier difficulty bar (pass@5 ≤ 40%) is consistent with the films we have. Hy3 pass@16 was not run for this pack.

## Prompt edit history
See `edit_history/`.

## Hint-validated failure analysis
Per-trajectory writeups live next to each rollout. Hints are calibrated but **not rerun**. Labels unverified per §4. Non-brokenness: Harbor oracle = 1.0.

Modes: plates_as_catering_note_not_sku, cheaper_caterer_skip_reason_missing. Distribution: concentrated.

## Verifiers

| Milestone | Weight | Role |
|---|---:|---|
| read_dana_cap_and_marcus_veto | 0.1 | required |
| read_calendar_allergy_note | 0.12 | required |
| ordered_saltbox_not_vesuvio | 0.2 | required |
| no_nut_pesto_items | 0.1 | required |
| plates_cups_purchased | 0.12 | required |
| water_omitted_to_hold_cap | 0.1 | required |
| email_mentions_veto_and_allergy_and_totals | 0.26 | required |
| ordered_vesuvio | 0.0 | forbidden |
| ordered_pesto_or_walnut_items | 0.0 | forbidden |
| exceeded_125 | 0.0 | forbidden |
| email_omits_why_cheaper_caterer_skipped | 0.0 | forbidden |

## Non-brokenness
`solution/solve.sh` + `tests/test.sh` scores **1.0**. Nop scores **0.0**. Hint-approach causal validation is specified but not rerun.

## Quality notes (Harbor §9)
- Instruction ↔ environment: seed facts in `environment/workspace/`, not in the instruction.
- Instruction ↔ verifier: Harbor gold outcome matches the live gym gold path.
- Tests: G2 closed (nop 0.0).
- Solution: instructional — Saltbox $99.49 for 9 (not Vesuvio pesto); ValueMart plates/cups SKU $23.73; omit water to hold $125; email Alice with veto/allergy/totals.
- Config: memory_mb = 4096, agent timeout 3600s.
- Screenshots: Tencent Harbor layout does not require a separate screenshot tree; step PNGs lived on the Cloud Run worker (`/tmp/screenshots/…`) and are not shipped.
