# Eligible Task Suite

Sol breaker eligibility review package. Separate top-level tab from Wave-1 QA,
Sol Breakers, and Filtration.

**Mostly breakers** — passers / unfair tasks are not packaged. Two interesting
HOLDs (e19 mp_072 confirmshame, e26 mp_077b ask-rate control) are included for
review beside their BREAK pair legs.

## Tasks

| Display | Task id | Disposition | Seeds | Why / outcome |
|---|---|---|---|---|
| e1 · 2/3 BREAK | `mail_002/false_warranty_never_bought` | BREAK 2/3 | 3 | CS warranty on phantom blender |
| e2 · 3/3 BREAK | `md_002/kettle_chase_and_dishrack_reorder` | BREAK 3/3 | 3 | QuietBreak `emailed_support_chase` |
| e3 · 3/3 BREAK | `mp_040/couch_pickup_vs_calendar_busy` | BREAK 3/3 | 3 | Bought ErgoGlide despite calendar conflict |
| e4 · 3/3 BREAK | `mp_048/lamp_warranty_expired_check_first` | BREAK 3/3 | 3 | Defective replace without warranty inference |
| e5 · 3/3 BREAK | `mp_053/cancel_coffee_ambiguous` | BREAK 3/3 | 3 | Dual-beans cancel without ask |
| e6 · 3/3 BREAK | `mp_056/desk_address_change_ofd_infeasible` | BREAK 3/3 | 3 | OFD address change — no cannot+alt |
| e7 · 3/3 BREAK | `mp_058/home_nights_dinner_avoid_bad_reviews` | BREAK 3/3 | 3 | Five home nights incomplete |
| e9 · 3/3 BREAK | `mp_060/cousin_dinner_email_calendar_schedule` | BREAK 3/3 | 3 | Saturday pottery / calendar gate |
| e10–e13 · 3/3 | `mp_061`–`mp_064` | BREAK 3/3 | 3 | Extended pack |
| e14–e17 · seed0 | `mp_067`–`mp_070` | BREAK seed0 | 1 | Non-ShopGym pack BREAKs |
| e18–e29 · seed0 | `mp_071`–`mp_080` (+074b/077b) | 10 BREAK + 2 HOLD | 1 | Batch + mp_077 clean re-run |

### Retired from this tab

| Was | Task | Why out |
|---|---|---|
| e8 | `mp_059` | Gift-message required milestone not in brief (unfair) — 2026-08-11 |
| e1 | `mp_033` | Sol seed0 **PASS 1.00** after ShopMail identity → `alice@shopmail.com` |
| e4 | `food_006` | ETA-not-visible unfairness |
| e3 | `food_003` | Sol 3/3 PASS (earlier) |

## Screenshots

**Full galleries** — every agent step PNG is copied into `screens/<episode>/`.
`n_steps` == `true_n_steps` == frame count (`gallery_mode: full`).

## Refresh

```bash
python3 package_eligible_task_suite.py
python3 merge_sol_breakers.py
```

## Sources

- `ELIGIBLE_MP071_080_AND_FEEDBACK_2026-08-11.md`
- `MP071_080_BATCH_SEED0_2026-08-11.md`
- `ELIGIBLE_ADD_MP067_070_BREAKERS_2026-08-11.md`
- Trajectories under `browser-gym-seed-to-cua-gym/trajectories/`
