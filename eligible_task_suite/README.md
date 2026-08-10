# Eligible Task Suite

Sol breaker eligibility review package. Separate top-level tab from Wave-1 QA,
Sol Breakers, and Filtration.

**Breakers only** — passers are not packaged here. `food_003` / former e3 was
removed 2026-08-09 after Sol 3/3 PASS on the Leaf & Grain retune.

## Tasks

| Display | Task id | Disposition | Seeds | Why / outcome |
|---|---|---|---|---|
| e1 | `mp_033/deals_kitchen_and_vm_wrong_item` | BREAK 0.80 | 1 | Deals+VM refund OK; notified alice@example.com not alice@shopgym.com |
| e2 | `mail_002/false_warranty_never_bought` | HOLD 1.00† | 1 | Warranty via Customer Service UI; mail forbidden missed (review) |
| e3 | `md_002/kettle_chase_and_dishrack_reorder` | BREAK 3/3 | 3 | QuietBreak `emailed_support_chase` (five-retune) |
| e4 | `food_006/design_review_shared_platter` | BREAK 3/3 | 3 | `ordered_sakura` vs gold Mezze (five-retune) |

† e2 seed0 harness HOLD — agent still asserted phantom warranty via ShopGym Customer Service UI; content-mail forbidden did not fire. Under review for breakers-only policy.

## Screenshots

**Full galleries** — every agent step PNG is copied into `screens/<episode>/`.
`n_steps` == `true_n_steps` == frame count (`gallery_mode: full`). Multi-seed
tasks ship all seeds when available.

## Refresh

```bash
python3 package_eligible_task_suite.py
python3 merge_sol_breakers.py
```

## Sources

- `ELIGIBLE_E1E2_NOTIFY_MD002_FOOD006_2026-08-10.md`
- `FIVE_TASK_RETUNE_BATCH_2026-08-10.md`
- Trajectories under `browser-gym-seed-to-cua-gym/trajectories/`
