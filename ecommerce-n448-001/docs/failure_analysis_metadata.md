# Failure analysis metadata — n448_allergy_safe_friday_lunch_nine

## (1) Methodology

### Failure mode taxonomy
- `plates_as_catering_note_not_sku`
- `cheaper_caterer_skip_reason_missing`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (buy the supply SKU) without naming ValueMart plates $23.73.

## (2) Distribution

This task is **concentrated** on 2 mode(s): `plates_as_catering_note_not_sku`, `cheaper_caterer_skip_reason_missing`. n=5 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
