# Failure analysis — rollout 2 (seed 1, episode a144536b)

**Reward:** 0.0 · BREAK · 80 steps · `same`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** m346 seeds 1-2
**Coverage note:** 3/3 Sol BREAK 0.00 (seeds 0–2). Not 5/5. Seeds 3–4 were in the remaining job; not on disk yet.

## Identified failure modes

- `stuck_on_ambient_food_cart`
- `never_reached_privacy_fork`

Observed: same.

## Hint (Section 4)

**Hint text:** The hospitality order is a seeded interview lunch item, and each candidate needs their own message — not one thread.

**Calibration:** Names the class (seeded SKU + separate messages) without listing the three addresses. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
