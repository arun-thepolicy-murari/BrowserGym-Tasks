# Gym-side fixes — copies of files that live outside version control

`browser-gym-seed-to-cua-gym/` is a separate checkout, it is **gitignored** by this repo,
and it has no `.git` of its own. So the changes below are tracked nowhere. These are
verbatim copies, kept here so they survive a re-clone of the gym; copy them back over the
gym checkout, or better, commit them in the gym's own repository.

```bash
cp -r _gym_patches/tools/. browser-gym-seed-to-cua-gym/tools/
```

## What changed and why

### `tools/seed_to_cuagym.py` — `transform_shop()`

The projection collapsed the cart to `{productId, quantity}`, dropping `gift_message`,
`gift_wrap`, `ship_to_address_id` and `scheduled_delivery`, and merging distinct lines of
the same product into one.

That silently disarmed the trap on **M75, M83, M87, M95, M97 and M99 — 18 of the 42
task/seeds.** The patched Amazon mock reads those exact field names off each cart line
(`amazon_mock_bridged.patch`, `Cart.jsx`), and the gym's `/api/cart/update` takes the same
names — `bridge.py` even warns in a comment that dropping them "silently defangs the
gift/split-shipping breaker tasks". The write half honoured that; the read half did not.

Lines now carry their options and their `lineId`, and only genuinely identical lines merge,
so a split-shipping cart stays two lines rather than becoming one of quantity 2.

### `tools/bridge.py` — `sid_for()` + `Bridge.default_sid()`

The default session id was `seed-<task_id>-<seed>-<app>`, and a gym `task_id` contains a
slash (`M73/expired_card_checkout`). A mock persists a session as `.mock-states/<sid>.json`,
where a slash is a path separator, not a character. `sid_for()` slugifies it, and is now the
single place any caller should build a sid.

### `tools/bridge_service.py` — `/bridge/reset` response

Returns `sids`, `mocks` and `pushed` alongside the state. Callers previously had to
reconstruct the sid scheme by hand (and `seed_to_cuagym --mock-map` mints a random uuid4
instead, which never matches what the bridge pushed to — that mismatch is why the first
live link opened an empty session). The annotator's in-app "Make this task live" button
also depends on this response to build its URLs.

### `tools/newui_harness_smoke.py` — default `APP_ORIGINS`

Defaulted to `shop=5203, mail=5401`. 5203 is Gmail and nothing listens on 5401, so shop was
pointed at the mail mock. Now `shop=5201, mail=5203`, matching the port table.

### `tools/PILOT_SETUP.md` — ports and the sid claim

Three examples disagreed with the file's own port table (`mail=5199`, and an
`--app-origins` line using 5203/5401/5301/5402/5403). Also corrected the claim that "the
annotator's `seed_sid` scheme matches the gym seeder exactly" — it did not; the two schemes
are now documented explicitly.
