# Failure analysis — rollout 3 (seed 2, episode 535adf00)

**Reward:** 0.3 · BREAK · 88 steps · `stuck on ShopGym mat`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** confirmed_5seed OLDER longer BRIEF
**Coverage note:** 5/5 Sol on OLDER longer BRIEF; live shorter BRIEF has seed0 film only (4261ed68). Remaining-job seeds 1–4 on live BRIEF not on disk yet.

## Identified failure modes

- `shopgym_mat_first`
- `alice_store_charges_email_missed`

Observed: stuck on ShopGym mat.

## Hint (Section 4)

**Hint text:** Compare delivered price and arrival day across stores before buying the first listing you see, and the brief still wants a close-out email with each store's charge.

**Calibration:** Names the class (delivered cost + ETA + close-out email) without naming Sunday / $40.71 / $111.79. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
