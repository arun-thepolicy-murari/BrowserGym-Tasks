# Failure analysis metadata — fb4_home_office_claim_omit_cancelled_chair

## (1) Methodology

### Failure mode taxonomy
- `trusted_lying_cancel_email`
- `inbox_only_no_orders_page`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (verify cancel vs charged) without naming $329 / $810.49.

## (2) Distribution

This task is **concentrated** on 2 mode(s): `trusted_lying_cancel_email`, `inbox_only_no_orders_page`. n=5 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
