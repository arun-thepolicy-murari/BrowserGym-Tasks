# Failure analysis metadata — breaker-10

## (1) Methodology

### Failure mode taxonomy
- `false_premise_accepted_as_fact` — treats a user claim as true without checking the account.
- `warranty_filed_for_never_bought_sku` — files support/warranty for a phantom item.
- `missing_sku_never_mentioned` — reports the visible order, omits the never-ordered item.
- `trusted_lying_cancel_email` — inbox cancel copy overrides the still-charged order.
- `inbox_only_no_orders_page` — never opens Your Orders.
- `plates_as_catering_note_not_sku` — writes supplies into food notes instead of buying them.
- `shopgym_mat_first` — buys the worse-delivered listing first.
- `alice_store_charges_email_missed` — gold cart, no close-out email.
- `false_premise_corrected_then_still_spent` — tells the user the truth, then buys anyway.
- `stuck_on_ambient_food_cart` — never places the seeded lunch.
- `wait_instead_of_ask` — reads the constraint, does not send the clarifying question.
- `return_ui_not_persisted` — reorder without a landed return.
- `bought_cheaper_store_missed_fee_email` — right store, incomplete all-in comparison.

Plus the published BrowserGym six-class tags used as one primary tag per task (Chezelles et al. arXiv:2412.05467 §5.8).

### Analysis methodology
Gym JSONL + scorecards + CONFIRMED_5SEED / UI031 / D460 audits.

### Validation pipeline
Hints are written at sweet-spot altitude and **not rerun**. Labels unverified. Oracle 1.0 is the non-brokenness demonstration (Tencent §3 / §4).

### QA
Scores cross-checked against gym `verifier_result` when the JSONL is present, and against GCS scorecards when only those exist.

## (2) Distribution

Dominant modes: false-premise / missing-SKU / omitted close-out email / trusted-inbox-over-ledger. Concentrated per task (1–2 modes), diverse across the 10.

| Distinct failure modes on the task | Number of tasks |
|---:|---:|
| 1 | 2 |
| 2 | 8 |
| 3 | 0 |
| 4 | 0 |
| 5 | 0 |
