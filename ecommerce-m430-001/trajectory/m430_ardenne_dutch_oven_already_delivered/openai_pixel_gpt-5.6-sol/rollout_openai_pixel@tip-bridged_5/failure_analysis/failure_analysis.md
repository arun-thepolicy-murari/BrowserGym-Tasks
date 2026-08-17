# Failure analysis — rollout 5 (seed 4, episode 7c35b1bf)

**Reward:** 0.8 · BREAK · 46 steps · `told Alice then bought replacement`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** remaining 5-seed GCS artifacts
**Coverage note:** 5/5 Sol BREAK 0.80 on live BRIEF (all five full trajs; seeds 1–4 recovered from remaining-job GCS artifacts)

## Identified failure modes

- `false_premise_corrected_then_still_spent`

Observed: told Alice then bought replacement.

## Hint (Section 4)

**Hint text:** If the user's 'never arrived' claim is wrong, the close-out is to say so and stop. A replacement is not required once the original is located.

**Calibration:** Names the class (don't spend after disproving the premise) without naming Vassiliou / mail room. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
