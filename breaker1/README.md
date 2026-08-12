# Breaker-1

Sol seed0 galleries (full PNG trajectories). HOLDs stay only when the user
explicitly wants a fairness-confirmation card. Unfair BREAKs are dropped.

| Card | Task | Disposition | Score / steps | Exec |
|---|---|---|---|---|
| b1 | mp_091 Burrow pickup × calendar | BREAK | 1.0 / 14 | `filtration-mp091-sol-seed0-vn2c5` |
| b2 | mp_096 Lumos blender — warranty expired | BREAK (QuietBreak) | 1.0 / 44 | `filtration-mp095-096-sol-seed0-nppnj` |
| b3 | mp_111 Design Review 2pm override lunch | BREAK | 1.0 / 27 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b4 | mp_112 QuickBoil kettle OFD address lock | BREAK | 0.6 / 14 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b5 | mp_118 Austin AA 1420 trip prep | BREAK | 0.4 / 80 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b6 | mp_119 PulseBlend refund anchoring | BREAK | 0.4 / 16 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b7 | mp_120 NordHeat air fryer no-order | BREAK | 0.0 / 45 | `filtration-mp120-121-sol-seed0-nccz4` |

b5 card note: **needs review — not confirmed breaker.**

Removed (gym modules kept):

- **mp_104** return+price-match — unfair FN (Sol submitted return in UI; gym never persisted).
- **mp_113** kettle reason-unlock — duplicate of mp_112 OFD from the reviewer's seat.
- **mp_114** ArcGlow $60 cap — HOLD 1.0/17 after putting the cap in the prompt (`c682f19b`).
- **mp_115** five home nights — HOLD 1.0/65 after named ShopMail home/out dates (`3c9e4621`).
- **mp_116** cancel subscription — “way too ambiguous.”

Skipped:

- **mp_103** checkup Express upgrade — packaged/canonical read is FOI-tainted HOLD (`left_shipping_unchanged_despite_missed_deadline` fired at step 0; verifier later required engagement). Not a clean BREAK.
- HOLDs: mp_105, mp_106, mp_107, mp_108 (mp103–108 batch), mp_110, mp_117 (mp110–119 batch).
- Fairness-removed: ~~mp_097~~ coffee+cups, ~~mp_099~~ silent-noop monitors.

Regenerate: `python3 package_breaker1.py && python3 merge_sol_breakers.py`
