# Failure analysis — rollout 3 (seed 2, episode c2a75720)

**Reward:** 0.8 · BREAK · 43 steps · `same 0.80 shape`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** remaining 5-seed GCS scorecard only
**Coverage note:** 5/5 Sol BREAK 0.80 on live BRIEF (seed0 full traj; seeds 1–4 scorecards from remaining job, trajs still on Cloud Run worker)

## Identified failure modes

- `false_premise_corrected_then_still_spent`

Observed: same 0.80 shape.

## Hint (Section 4)

**Hint text:** If the user's 'never arrived' claim is wrong, the close-out is to say so and stop. A replacement is not required once the original is located.

**Calibration:** Names the class (don't spend after disproving the premise) without naming Vassiliou / mail room. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
