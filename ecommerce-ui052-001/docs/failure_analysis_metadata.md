# Failure analysis metadata — ui_052_jacket_return_reorder_large

## (1) Methodology

### Failure mode taxonomy
- `return_ui_not_persisted`
- `reorder_without_return`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (return + reorder as two actions) without naming Medium/Large.

## (2) Distribution

This task is **concentrated** on 2 mode(s): `return_ui_not_persisted`, `reorder_without_return`. n=5 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
