# Failure analysis — rollout 3 (seed 2, episode d39a7571)

**Reward:** 0.22 · BREAK · 87 steps · `never ordered Saltbox`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** n448 seeds 1-4
**Coverage note:** 5/5 Sol on live BRIEF

## Identified failure modes

- `plates_as_catering_note_not_sku`
- `cheaper_caterer_skip_reason_missing`

Observed: never ordered Saltbox.

## Hint (Section 4)

**Hint text:** Kitchen supplies the brief asked for have to be purchased as their own store items if a catering note will not actually produce them.

**Calibration:** Names the class (buy the supply SKU) without naming ValueMart plates $23.73. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
