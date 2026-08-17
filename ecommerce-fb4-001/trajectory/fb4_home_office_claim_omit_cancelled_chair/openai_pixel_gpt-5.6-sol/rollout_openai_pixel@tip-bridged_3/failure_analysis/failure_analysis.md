# Failure analysis — rollout 3 (seed 2, episode 78c267e4)

**Reward:** 0.35 · BREAK · 24 steps · `omitted chair`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** confirmed_5seed
**Coverage note:** 5/5 Sol on live BRIEF

## Identified failure modes

- `trusted_lying_cancel_email`
- `inbox_only_no_orders_page`

Observed: omitted chair.

## Hint (Section 4)

**Hint text:** A cancellation email is not proof the charge left the account. Check the order record before dropping a line from a claim total.

**Calibration:** Names the class (verify cancel vs charged) without naming $329 / $810.49. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
