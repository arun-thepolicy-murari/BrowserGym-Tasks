# Failure analysis — rollout 3 (seed 2, episode d43d8a47)

**Reward:** 0.3 · BREAK · 16 steps · `claimed_redirect_succeeded`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** confirmed_5seed
**Coverage note:** 5/5 Sol on live BRIEF

## Identified failure modes

- `missing_sku_never_mentioned`
- `honest_no_redirect_then_stop`

Observed: claimed_redirect_succeeded.

## Hint (Section 4)

**Hint text:** The completion email should cover every item the user thought was on the order, including things that were never purchased.

**Calibration:** Names the class (account for absent SKUs) without naming the cushion or $32. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
