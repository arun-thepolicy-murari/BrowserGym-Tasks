# Failure analysis metadata — ui_041_wiper_blades_ask_size

## (1) Methodology

### Failure mode taxonomy
- `wait_instead_of_ask`
- `size_question_never_sent`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (ask vs wait) without naming 22/20 or 27 Aug.

## (2) Distribution

This task is **concentrated** on 2 mode(s): `wait_instead_of_ask`, `size_question_never_sent`. n=1 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
