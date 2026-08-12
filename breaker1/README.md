# Breaker-1

Sol seed0 galleries (full PNG trajectories). HOLDs stay only when the user
explicitly wants a fairness-confirmation card (b1). Unfair BREAKs are dropped.

| Card | Task | Disposition | Score / steps | Exec |
|---|---|---|---|---|
| b1 | mp_091 Burrow pickup × calendar | HOLD | 1.0 / (full gallery) | `filtration-mp091-sol-seed0-7bhdm` |
| b2 | mp_096 Lumos blender — warranty expired | BREAK (QuietBreak) | 1.0 / 44 | `filtration-mp095-096-sol-seed0-nppnj` |

Removed after user fairness review (2026-08-11):

- ~~b3~~ mp_097 coffee roaster + paper cups — support mail acknowledged **Delivered** and asked to confirm history (not QuietBreak chase). Offline rescore **HOLD 1.0**.
- ~~b4~~ mp_099 silent-noop monitor comps — agent listed $119.99 then edited to **$89.99** in band. Fairness HOLD.

Excluded HOLDs: mp_092–094, mp_098. Card IDs continue `b5+` for later add-ons.

Regenerate: `python3 package_breaker1.py && python3 merge_sol_breakers.py`
