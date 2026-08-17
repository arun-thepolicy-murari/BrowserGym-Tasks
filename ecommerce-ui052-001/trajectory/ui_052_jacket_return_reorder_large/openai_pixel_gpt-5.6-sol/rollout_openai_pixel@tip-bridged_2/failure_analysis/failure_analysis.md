# Failure analysis — rollout 2 (seed 1, episode 16ab0085)

**Reward:** 0.65 · BREAK · 24 steps · `bought Large; Medium return never landed`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** remaining 5-seed GCS artifacts
**Coverage note:** 5/5 Sol BREAK 0.65 on live BRIEF (all five full trajs; seeds 1–4 recovered from remaining-job GCS artifacts)

## Identified failure modes

- `return_ui_not_persisted`
- `reorder_without_return`

Observed: bought Large; Medium return never landed.

## Hint (Section 4)

**Hint text:** The brief asks for two commits: start the return from Returns & Orders, then buy the other size from the product variant picker.

**Calibration:** Names the class (return + reorder as two actions) without naming Medium/Large. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
