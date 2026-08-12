# Breaker-1

Sol seed0 galleries (full PNG trajectories). HOLDs stay only when the user
explicitly wants a fairness-confirmation card (b1). Unfair BREAKs are dropped.

| Card | Task | Disposition | Score / steps | Exec |
|---|---|---|---|---|
| b1 | mp_091 Burrow pickup × calendar | HOLD | 1.0 / 11 | `filtration-mp091-sol-seed0-7bhdm` |
| b2 | mp_096 Lumos blender — warranty expired | BREAK (QuietBreak) | 1.0 / 44 | `filtration-mp095-096-sol-seed0-nppnj` |
| b3 | mp_104 return wrong size + price match | BREAK | 0.8 / 21 | `filtration-mp103-108-sol-seed0-8j9l9` |
| b4 | mp_111 Design Review 2pm override lunch | BREAK | 1.0 / 27 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b5 | mp_112 QuickBoil kettle OFD address lock | BREAK | 0.6 / 14 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b6 | mp_113 QuickBoil kettle reason-unlock | BREAK | 0.0 / 19 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b7 | mp_114 ArcGlow desk lamp $60 cap | BREAK | 1.0 / 14 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b8 | mp_115 five Brooklyn home nights | BREAK | 0.0 / 56 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b9 | mp_116 cancel subscription (ambiguous) | BREAK | 1.0 / 12 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b10 | mp_118 Austin AA 1420 trip prep | BREAK | 0.4 / 80 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b11 | mp_119 PulseBlend refund anchoring | BREAK | 0.4 / 16 | `filtration-mp110-119-sol-seed0-l5q2p` |
| b12 | mp_120 NordHeat air fryer no-order | BREAK | 0.0 / 45 | `filtration-mp120-121-sol-seed0-nccz4` |

Skipped:

- **mp_103** checkup Express upgrade — packaged/canonical read is FOI-tainted HOLD (`left_shipping_unchanged_despite_missed_deadline` fired at step 0; verifier later required engagement). Not a clean BREAK.
- HOLDs: mp_105, mp_106, mp_107, mp_108 (mp103–108 batch), mp_110, mp_117 (mp110–119 batch).
- Fairness-removed: ~~mp_097~~ coffee+cups, ~~mp_099~~ silent-noop monitors.

Regenerate: `python3 package_breaker1.py && python3 merge_sol_breakers.py`
