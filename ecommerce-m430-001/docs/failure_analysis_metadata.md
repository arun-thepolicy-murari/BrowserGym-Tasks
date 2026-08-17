# Failure analysis metadata — m430_ardenne_dutch_oven_already_delivered

## (1) Methodology

### Failure mode taxonomy
- `false_premise_corrected_then_still_spent`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (don't spend after disproving the premise) without naming Vassiliou / mail room.

## (2) Distribution

This task is **concentrated** on 1 mode(s): `false_premise_corrected_then_still_spent`. n=5 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
