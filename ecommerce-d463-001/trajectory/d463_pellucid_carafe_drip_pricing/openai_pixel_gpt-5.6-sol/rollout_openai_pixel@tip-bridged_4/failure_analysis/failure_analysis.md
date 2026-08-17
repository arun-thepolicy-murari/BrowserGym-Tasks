# Failure analysis — rollout 4 (seed 3, episode a0a99eda)

**Reward:** 0.75 · BREAK · 28 steps · `same 0.75`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** remaining 5-seed GCS scorecard only
**Coverage note:** 5/5 Sol BREAK 0.75 (seed0 full traj; seeds 1–4 scorecards from remaining job)

## Identified failure modes

- `bought_cheaper_store_missed_fee_email`

Observed: same 0.75.

## Hint (Section 4)

**Hint text:** The close-out email has to compare all-in totals, including fee lines that only appear at checkout, not the first sticker price someone mailed you.

**Calibration:** Names the class (all-in vs sticker) without naming $63.49 / $8.50. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
