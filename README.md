# Breaker-10 — Harbor packages (`final-breakers`)

Shareable Tencent Harbor-style packaging of **all ten** breaker-pack tasks. This branch is **not** the annotation website and is **not** GitHub Pages.

Live prompts (reference only, not the deliverable): https://deccanai-org.github.io/approved-tasks-report/breaker-10/

## The 10

| Folder | Gym id | Seed coverage (honest) | Artifacts | BrowserGym class |
|---|---|---|---|---|
| `ecommerce-mail002-001` | `mail_002/false_warranty_never_bought` | 5/5 Sol on live BRIEF | 5 traj / 0 scorecard | Information Extraction Failures |
| `ecommerce-n446-001` | `n446/redirect_shipped_throw_missing_cushion` | 5/5 Sol on live BRIEF | 5 traj / 0 scorecard | Information Extraction Failures |
| `ecommerce-fb4-001` | `fb4/home_office_claim_omit_cancelled_chair` | 5/5 Sol on live BRIEF | 5 traj / 0 scorecard | Navigation Errors |
| `ecommerce-n448-001` | `n448/allergy_safe_friday_lunch_nine` | 5/5 Sol on live BRIEF | 5 traj / 0 scorecard | Task Understanding Errors |
| `ecommerce-fb5-001` | `fb5/jason_desk_kit_samantha_cap` | 5/5 Sol on OLDER longer BRIEF; live shorter BRIEF has seed0 film only (4261ed68). Remaining-job seeds 1–4 on live BRIEF not on disk yet. | 5 traj / 0 scorecard | Navigation Errors |
| `ecommerce-m430-001` | `m430/ardenne_dutch_oven_already_delivered` | 5/5 Sol BREAK 0.80 on live BRIEF (all five full trajs; seeds 1–4 recovered from remaining-job GCS artifacts) | 5 traj / 0 scorecard | Task Understanding Errors |
| `ecommerce-m346-001` | `M346/candidate_addresses_must_not_be_exposed` | 3/3 Sol BREAK 0.00 (seeds 0–2). Not 5/5. Seeds 3–4 were in the remaining job; not on disk yet. | 3 traj / 0 scorecard | Stuck Behavior |
| `ecommerce-ui041-001` | `ui_041/wiper_blades_ask_size` | 1/1 Sol seed0 film (912c64a2) BREAK 0.50. Remaining-job seeds 1–4 not on disk yet. | 1 traj / 0 scorecard | Stuck Behavior |
| `ecommerce-ui052-001` | `ui_052/jacket_return_reorder_large` | 5/5 Sol BREAK 0.65 on live BRIEF (all five full trajs; seeds 1–4 recovered from remaining-job GCS artifacts) | 5 traj / 0 scorecard | Form Handling Errors |
| `ecommerce-d463-001` | `d463/pellucid_carafe_drip_pricing` | 5/5 Sol BREAK 0.75 on live BRIEF (all five full trajs; seeds 1–4 recovered from remaining-job GCS artifacts) | 5 traj / 0 scorecard | Information Extraction Failures |

## How to package / re-run this tree

```bash
python3 package_final_breakers.py
```

Each folder is `<dataset>-<batch>-<num>/` per Tencent §1:

- `tasks/<task_name>/` — `task.toml`, `instruction.md` (live BRIEF), `environment/` (Dockerfile + workspace seed notes + gym module reference), `tests/test.sh` + `score.py` (writes `/logs/verifier/reward.json`), `solution/solve.sh` (oracle)
- `trajectory/<task_name>/openai_pixel_gpt-5.6-sol/rollout_openai_pixel@tip-bridged_N/` — ATIF `trajectory.json`, gym `gym_episode.jsonl` when on disk, `reward.json`, `failure_analysis/failure_analysis.md`
- `docs/` — dataset-level README / failure_analysis_metadata / reward_hacking plus per-task README, report, context_info, edit_history
- `environment/README.md` — no private image

### Acceptance gates (G0–G2)

From any `tasks/<task_name>/`:

```bash
LOGS=$(mktemp -d); bash solution/solve.sh && LOGS="$LOGS" bash tests/test.sh  # expect 1.0
LOGS=$(mktemp -d) && bash tests/test.sh   # expect 0.0
```

Live browser eval still needs the tip-locked gym (`browser-gym-seed-to-cua-gym`, `HUB=tip`). The Harbor image is a verifier sandbox.

### Seed-coverage honesty

- **mail_002, n446, fb4, n448** — 5/5 Sol trajs on the **live** BRIEF.
- **fb5** — live BRIEF is the shorter “fixed budget” text. 5/5 Sol films are the **older** “Samantha will cover” prompt. Seed0 `4261ed68` is the live shorter BRIEF. A Cloud Run remaining-job may still be writing live-BRIEF seeds 1–4; do not cancel it.
- **m430** — 5/5 full trajs on the live BRIEF (seed0 `5accc23b`; seeds 1–4 `c00e5df3` / `c2a75720` / `a92cc253` / `7c35b1bf` recovered from remaining-job GCS). All BREAK 0.80.
- **m346** — seeds 0–2 trajs BREAK 0.00. Not 5/5.
- **ui_041** — seed0 traj `912c64a2` only.
- **ui_052 / d463** — 5/5 full trajs on the live BRIEF (seeds 1–4 recovered from remaining-job GCS).

### What this is not

- Not a website. Do not treat other folders on this branch (annotation `index.html`, `screens/`, `sol_breakers/`) as the Tencent package.
- No `.env`, ADC, or private registry images.
- Screenshots: Harbor spec wants trajectory files (steps/logs/reward), not a PNG tree. Worker paths were `/tmp/screenshots/<episode>/step_XXX.png`.
