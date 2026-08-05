# Filtration 28/47 — Phase 2 Dual Breakers

Showcase catalog for **Tencent filtration Phase 2** dual-model confirmed breakers
(Sol `gpt-5.6-sol` × Opus `claude-opus-5`, credit-adjusted).

**Bar:** Sol BREAK ≥2/5 **and** Opus BREAK ≥2/5 on non-credit seeds.

| Panel | Confirmed |
|---|---|
| Sample 20 | **10 / 20** |
| Remaining 27 | **18 / 27** |
| **Combined** | **28 / 47** |

Pool outcomes (full 47): 28 dual / 14 Sol-only / 3 Opus-only / 2 INCONC (`M95`, `M366` — not shown).

## Contents

| File | Role |
|---|---|
| `tasks.json` | Lightweight showcase catalog (briefs + scores + domain/vein) |

## Refresh

```bash
python3 merge_sol_breakers.py
```

Preserves Wave-1 QA + Sol Breakers; replaces the `phase2_dual_breakers` pool from this folder.

## Source audits

- `TENCENT_FILTRATION_PHASE2_FULL47_REPORT_2026-08-05.md`
- `TENCENT_FILTRATION_PHASE2_SAMPLE20_2026-08-04.md`
- `TENCENT_FILTRATION_PHASE2_SAMPLE20_OPUS_CREDITFIX_2026-08-04.md`
- `TENCENT_FILTRATION_PHASE2_REMAINING27_2026-08-05.md`

Briefs from `ecommerce-browser-gym/server/tasks.py` `BRIEFS`. No full trajectory packaging in this pass.
