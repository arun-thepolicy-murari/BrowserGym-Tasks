# Failure analysis metadata — fb5_jason_desk_kit_samantha_cap

## (1) Methodology

### Failure mode taxonomy
- `shopgym_mat_first`
- `alice_store_charges_email_missed`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (delivered cost + ETA + close-out email) without naming Sunday / $40.71 / $111.79.

## (2) Distribution

This task is **concentrated** on 2 mode(s): `shopgym_mat_first`, `alice_store_charges_email_missed`. n=5 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
