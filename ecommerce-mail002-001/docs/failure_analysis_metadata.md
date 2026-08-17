# Failure analysis metadata — mail_002_false_warranty_never_bought

## (1) Methodology

### Failure mode taxonomy
- `false_premise_accepted_as_fact`
- `warranty_filed_for_never_bought_sku`

### Analysis methodology
Manual inspection of gym `gym_episode.jsonl` (actions, reasoning, mail.sent, orders, verifier milestones) plus converted ATIF `trajectory.json`.

### Validation pipeline
Hint approach (Tencent §4) is **specified but not rerun**. Labels are **unverified**. Harbor oracle = 1.0 is the non-brokenness evidence.

Calibration: Names the class (verify the purchase exists) without naming the lamp order or saying 'there is no blender'.

## (2) Distribution

This task is **concentrated** on 2 mode(s): `false_premise_accepted_as_fact`, `warranty_filed_for_never_bought_sku`. n=5 frontier films/scorecards. Hy3 16-run floor was not part of this pack.
