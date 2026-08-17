# Failure analysis metadata — n446_redirect_shipped_throw_missing_cushion

## (1) Methodology

### Failure mode taxonomy
- `missing_sku_never_mentioned`
- `honest_no_redirect_then_stop`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (account for absent SKUs) without naming the cushion or $32.

## (2) Distribution

This task is **concentrated** on 2 mode(s): `missing_sku_never_mentioned`, `honest_no_redirect_then_stop`. n=5 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
