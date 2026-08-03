# Sol Breakers — Bridged (annotation pool)

Confirmed Sol (`openai_pixel[gpt-5.6-sol]`) outcomes on the bridged environment
from 2026-08-02. Separate from the Wave-1 gpt-5.5 QA queue — do not merge into
`new_samples/`.

## Contents

| File | Role |
|---|---|
| `tasks.json` | Catalog of confirmed BREAK + silent-non-completion tasks |

## Display IDs (n#)

UI shows sequential **n1…n6**. Gym / audit ids stay in `original_mnum`, `slug`,
`task_id`, and `env.provenance.original_*`.

| Display | Original |
|---|---|
| n1 | lh_004 |
| n2 | M142 |
| n3 | cal_004 |
| n4 | md_002 |
| n5 | md_001 |
| n6 | mail_001 |

Order: CONFIRMED BREAKs first, then silent-non-completion.

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
- `MAIL001_SOL_BRIDGED_3SEED.md` / `MD001_SOL_BRIDGED_3SEED.md`
- Per-task audits under `ecommerce-browser-gym/docs/history/audits/`
