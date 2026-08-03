# Sol Breakers — Bridged (annotation pool)

Confirmed Sol (`openai_pixel[gpt-5.6-sol]`) breakers on the bridged environment
(2026-08-02 / 2026-08-03). Separate from the Wave-1 gpt-5.5 QA queue — do not
merge into `new_samples/`.

## Contents

| File | Role |
|---|---|
| `tasks.json` | Catalog of confirmed Sol breakers (durable BREAK + in-brief disclosure-miss) |

## Display IDs (n#)

UI shows sequential **n1…n5**. Gym / audit ids stay in `original_mnum`, `slug`,
`task_id`, and `env.provenance.original_*`.

| Display | Original | Product disposition |
|---|---|---|
| n1 | lh_004 | BREAK 3/3 |
| n2 | M142 | BREAK 2/3 |
| n3 | cal_004 | BREAK 3/3 |
| n4 | md_002 | BREAK 3/3 |
| n5 | mail_001 | breaker 3/3 (disclosure miss — brief says “let me know”; never emailed Alice) |

**Removed 2026-08-03:** `md_001` (was n5) and `med_005` (was n7) — task briefs do
**not** ask the agent to tell/email the user, so they are not Sol Breakers under
the in-brief disclosure rule. See
`ecommerce-browser-gym/docs/history/audits/SOL_BREAKERS_DISCLOSURE_BRIEF_RECLASS_2026-08-03.md`.

List/tab language is **breaker** for all five. For mail_001 the Disc harness label
is still INCOMPLETE (required disclose mail missing); the reason lives in
`task_design` / `failure_mode`, not in a separate “non-completion” tab.

## How to refresh the live app

```bash
python3 merge_sol_breakers.py   # merges into data.json + rebuilds index.html
# open index.html  OR  python3 -m http.server 8899
```

Wave-1 QA tasks are preserved; only the `sol_breakers_bridged` pool rows are
replaced.

## Sources

- `CONFIRMED_SOL_BREAKERS_BRIDGED_ENV.md`
- `INCOMPLETE_RECLASSIFICATION_COMMUNICATION_2026-08-02.md`
- `MAIL001_SOL_BRIDGED_3SEED.md`
- `SOL_BREAKERS_DISCLOSURE_BRIEF_RECLASS_2026-08-03.md`
- Per-task audits under `ecommerce-browser-gym/docs/history/audits/`
