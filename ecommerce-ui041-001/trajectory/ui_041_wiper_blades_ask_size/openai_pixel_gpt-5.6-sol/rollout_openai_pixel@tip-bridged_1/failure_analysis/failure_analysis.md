# Failure analysis — rollout 1 (seed 0, episode 912c64a2)

**Reward:** 0.5 · BREAK · 20 steps · `read service; bought nothing; never asked size`
**Harness:** openai_pixel@tip-bridged · gpt-5.6-sol
**Source:** ui031-ui060 seed0
**Coverage note:** 1/1 Sol seed0 film (912c64a2) BREAK 0.50. Remaining-job seeds 1–4 not on disk yet.

## Identified failure modes

- `wait_instead_of_ask`
- `size_question_never_sent`

Observed: read service; bought nothing; never asked size.

## Hint (Section 4)

**Hint text:** If the fitment is not in the account, the instruction already told you to ask before buying — waiting is not asking.

**Calibration:** Names the class (ask vs wait) without naming 22/20 or 27 Aug. Over-specified would name the gold SKU/price; under-specified would be “be careful.”

**Rerun outcome:** not executed in this package. Label remains **unverified** per Tencent §4 until a hint episode is run.

**Interpretation if a future hint run succeeds:** capability gap, not a broken environment. Harbor `solution/solve.sh` scores 1.0, so the task is solvable in principle.
