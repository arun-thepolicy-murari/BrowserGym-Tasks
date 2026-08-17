# Failure analysis — rollout 1 (seed 0, episode 72b00106)

**Reward:** 0.75 · BREAK · 25 steps · `bought VM $56; missed fee comparison email`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** d460-d481 seed0
**Coverage note:** 5/5 Sol BREAK 0.75 on live BRIEF (all five full trajs; seeds 1–4 recovered from remaining-job GCS artifacts)

## Identified failure modes

- `bought_cheaper_store_missed_fee_email`

Observed: bought VM $56; missed fee comparison email.

## Hint (Section 4)

**Hint text:** The close-out email has to compare all-in totals, including fee lines that only appear at checkout, not the first sticker price someone mailed you.

**Calibration:** Names the class (all-in vs sticker) without naming $63.49 / $8.50. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
