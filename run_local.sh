#!/usr/bin/env bash
# Bring up one (task, seed) on the NEW UIs, in BRIDGED mode.
#
#   ./run_local.sh                 # M73 seed 0
#   ./run_local.sh M100 2
#   ./run_local.sh --verify        # the gym's real milestone verdict, right now
#   ./run_local.sh --status
#   ./run_local.sh --stop
#
# What "bridged" means, and why it matters:
#
#   Seeding a mock (POST /post?sid=…) only makes it *show* a task's world. Clicks
#   then mutate the mock's own React store — placeOrder mints a fake `ord-<ts>`,
#   gift options live in localStorage, and the gym's verifier never sees any of it.
#   That is a UI shell, not an environment.
#
#   Bridged mode (?bridge=<url> on the page) routes every interactable through the
#   REAL gym engine: cross-app bus, scheduler, breaker traps, verifiers. So this
#   script starts FOUR things, not one:
#
#     gym      uvicorn server.main:app        :8077   the engine
#     bridge   tools.bridge_service           :8090   UI click -> gym action -> re-project
#     mocks    vite per website               :5201…  the realistic UIs
#     app      python -m http.server          :8899   the annotator
#
#   Ports, tokens and the app map are single-sourced here so they cannot drift
#   apart the way run_pilot.sh / PILOT_SETUP.md / newui_harness_smoke.py did.

set -euo pipefail
cd "$(dirname "$0")"

APP_PORT=8899
GYM_PORT="${GYM_PORT:-8077}"
BRIDGE_PORT="${BRIDGE_PORT:-8090}"
GYM_URL="http://127.0.0.1:$GYM_PORT"
BRIDGE_URL="http://127.0.0.1:$BRIDGE_PORT"

HUB="${HUB:-$PWD/CUA-Gym-Hub}"
GYM="$PWD/browser-gym-seed-to-cua-gym"
PY="${PY:-$PWD/_ref/venv/bin/python}"
[ -x "$PY" ] || PY=python3

TOKEN_FILE=".harness_token"
LOGDIR="${LOGDIR:-/tmp/newui}"
mkdir -p "$LOGDIR"

# gym-app : mock-dir : port
# Ports match tools/PILOT_SETUP.md. mail is 5203 (it was 5199 here, which meant
# every doc, smoke test and helper disagreed about where Gmail lives).
APPS=(
  "shop:amazon_mock:5201"
  "market:ebay_mock:5202"
  "mail:gmail_mock:5203"
  "calendar:google_calendar_mock:5204"
  "food:uber_eats_mock:5205"
)

# Deep-link form. "dual" puts the route in BOTH the path and the hash:
#
#     http://127.0.0.1:5201/cart?sid=…&bridge=…#/cart
#
# A BrowserRouter build reads the path (vite's SPA fallback serves index.html for
# any path, so /cart is not a 404); a HashRouter build ignores the path and reads
# the hash. Either way the tab lands on the page the agent saw at step 0. This
# replaces guessing at the router — the previous hash-only guess was wrong, and
# every link opened on the mock's home page instead.
#   hash | path — force one form if you ever need to.
ROUTE_STYLE="${ROUTE_STYLE:-dual}"

# ---------------------------------------------------------------- helpers ----
port_pids() { lsof -ti "tcp:$1" -sTCP:LISTEN 2>/dev/null || true; }
up()        { curl -sf -m2 -o /dev/null "$1" 2>/dev/null; }

# Detach a long-lived server from this shell's process group.
# macOS has no setsid(1); Python os.setsid() + double-fork survives Cursor/shell
# teardown (plain nohup/& still dies on SIGTERM to the group).
detach() { # detach <cwd> <logfile> <cmd> [args…]
  local cwd="$1" log="$2"; shift 2
  "$PY" - "$cwd" "$log" "$@" <<'PY'
import os, sys
cwd, log, *cmd = sys.argv[1:]
if os.fork():
    raise SystemExit(0)
os.setsid()
if os.fork():
    raise SystemExit(0)
os.chdir(cwd)
fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
os.dup2(fd, 1); os.dup2(fd, 2)
if fd > 2:
    os.close(fd)
devnull = os.open(os.devnull, os.O_RDONLY)
os.dup2(devnull, 0)
if devnull > 2:
    os.close(devnull)
os.environ.setdefault("PYTHONUNBUFFERED", "1")
os.execvp(cmd[0], cmd)
PY
}

wait_for() { # wait_for <url> <label> [tries]
  local n="${3:-60}"
  for _ in $(seq 1 "$n"); do up "$1" && return 0; sleep 0.5; done
  echo "  !! $2 never came up at $1 (log: $LOGDIR/)" >&2
  return 1
}

stop() {
  for a in "${APPS[@]}"; do IFS=: read -r _ _ p <<< "$a"; port_pids "$p" | xargs kill 2>/dev/null || true; done
  for p in "$APP_PORT" "$GYM_PORT" "$BRIDGE_PORT"; do port_pids "$p" | xargs kill 2>/dev/null || true; done
  rm -f live_env.json
  echo "stopped (gym, bridge, mocks, annotator)"
}

status() {
  printf '%-10s %-6s %s\n' SERVICE PORT STATE
  up "$GYM_URL/docs" || up "$GYM_URL/" \
    && printf '%-10s %-6s %s\n' gym "$GYM_PORT" up || printf '%-10s %-6s %s\n' gym "$GYM_PORT" DOWN
  up "$BRIDGE_URL/bridge/actions" \
    && printf '%-10s %-6s %s\n' bridge "$BRIDGE_PORT" up || printf '%-10s %-6s %s\n' bridge "$BRIDGE_PORT" DOWN
  up "http://127.0.0.1:$APP_PORT/index.html" \
    && printf '%-10s %-6s %s\n' annotator "$APP_PORT" up || printf '%-10s %-6s %s\n' annotator "$APP_PORT" DOWN
  for a in "${APPS[@]}"; do
    IFS=: read -r app dir p <<< "$a"
    if up "http://127.0.0.1:$p/"; then printf '%-10s %-6s %s\n' "$dir" "$p" up
    elif [ -x "$HUB/websites/$dir/node_modules/.bin/vite" ]; then printf '%-10s %-6s %s\n' "$dir" "$p" DOWN
    else printf '%-10s %-6s %s\n' "$dir" "$p" "no node_modules"; fi
  done
  [ -f live_env.json ] && { echo; echo "live_env.json:"; cat live_env.json; }
}

case "${1:-}" in
  --stop)   stop; exit 0 ;;
  --status) status; exit 0 ;;
  --verify)
    up "$BRIDGE_URL/bridge/actions" || { echo "bridge is not running — ./run_local.sh <MNUM> <seed> first" >&2; exit 1; }
    curl -s "$BRIDGE_URL/bridge/verify" | "$PY" -m json.tool
    exit 0 ;;
esac

MNUM="${1:-M73}"
SEED="${2:-0}"

# ------------------------------------------------- task id + start route -----
# One python call resolves the task and its per-seed start path, so the deep link
# lands where the agent started (13 of the 14 wave-1 tasks start at /cart; the
# old script always dropped the annotator on the home page instead).
read -r TASK_ID START_PATH <<< "$("$PY" - "$MNUM" "$SEED" <<'PY'
import json, sys
want, seed = sys.argv[1].upper(), sys.argv[2]
tasks = json.load(open("data.json"))["tasks"]
hit = next((t for t in tasks if t["mnum"].upper() == want), None)
if not hit:
    sys.exit(f"unknown task {want}. available: " + ", ".join(t["mnum"] for t in tasks))
env = hit.get("env") or {}
sd = (env.get("seeds") or {}).get(str(seed))
if sd is None:
    sys.exit(f"{want} has no seed {seed} (has: {', '.join(sorted((env.get('seeds') or {})))})")
print(hit["task_id"], sd.get("start_path") or "/")
PY
)"

[ -d "$HUB/websites/amazon_mock" ] || {
  echo "CUA-Gym-Hub not found at $HUB" >&2
  echo "Expected symlink 'CUA-Gym-Hub' -> …/CUA-Gym/hub, or pass HUB=/path" >&2
  exit 1
}

# The gym and the bridge must present the SAME /_harness/* token. Persist it so a
# re-run reuses the already-running gym instead of failing 401 against it.
if [ -s "$TOKEN_FILE" ]; then HARNESS_TOKEN="$(cat "$TOKEN_FILE")"
else HARNESS_TOKEN="$("$PY" -c 'import secrets;print(secrets.token_urlsafe(32))')"; printf %s "$HARNESS_TOKEN" > "$TOKEN_FILE"; chmod 600 "$TOKEN_FILE"; fi
export HARNESS_TOKEN

# ------------------------------------------------------------- 1. mocks ------
echo "mocks:"
MM_PARTS=() ; MOCK_PORT=()
for a in "${APPS[@]}"; do
  IFS=: read -r app dir port <<< "$a"
  if [ ! -x "$HUB/websites/$dir/node_modules/.bin/vite" ]; then
    echo "  skip $dir — npm install not done in $HUB/websites/$dir"
    continue
  fi
  if up "http://127.0.0.1:$port/"; then echo "  $dir already up on $port"
  else
    detach "$HUB/websites/$dir" "$LOGDIR/mock_$dir.log" \
      ./node_modules/.bin/vite --port "$port" --strictPort --host 127.0.0.1
    echo "  started $dir on $port"
  fi
  MM_PARTS+=("$app=http://127.0.0.1:$port")
  MOCK_PORT+=("$app:$port")
done
[ ${#MM_PARTS[@]} -gt 0 ] || { echo "no mock has node_modules — see tools/PILOT_SETUP.md step 3" >&2; exit 1; }

# --------------------------------------------------------------- 2. gym ------
if up "$GYM_URL/openapi.json"; then echo "gym already up on $GYM_PORT"
else
  export HARNESS_TOKEN
  detach "$GYM" "$LOGDIR/gym.log" \
    "$PY" -m uvicorn server.main:app --port "$GYM_PORT" --host 127.0.0.1 --log-level warning
  echo "gym starting on $GYM_PORT"
fi
wait_for "$GYM_URL/openapi.json" "gym"

# ------------------------------------------------------------ 3. bridge ------
# One bridge instance = one live episode (the gym holds a single global world), so
# a re-seed restarts it rather than resetting a stale one.
port_pids "$BRIDGE_PORT" | xargs kill 2>/dev/null || true
sleep 0.4
export GYM_URL HARNESS_TOKEN
export BRIDGE_TICK=1
for mp in "${MOCK_PORT[@]}"; do
  IFS=: read -r app port <<< "$mp"
  export "CUA_HUB_URL_$(echo "$app" | tr '[:lower:]' '[:upper:]')=http://127.0.0.1:$port"
done
detach "$GYM" "$LOGDIR/bridge.log" \
  "$PY" -m uvicorn tools.bridge_service:app --port "$BRIDGE_PORT" --host 127.0.0.1 --log-level warning
wait_for "$BRIDGE_URL/bridge/actions" "bridge"

# ----------------------------------------------------- 4. reset the episode --
# /bridge/reset builds the seed world, then push()es the projection into every
# mock tab. This replaces the old standalone `tools.seed_to_cuagym --mock-map`
# call, which seeded the mocks but left them disconnected from the engine.
echo "resetting $TASK_ID seed=$SEED …"
curl -s -X POST "$BRIDGE_URL/bridge/reset" -H 'Content-Type: application/json' \
     -d "{\"task_id\":\"$TASK_ID\",\"seed\":$SEED}" -o "$LOGDIR/reset.json"
"$PY" - "$LOGDIR/reset.json" <<'PY' || { echo "reset failed — see $LOGDIR/bridge.log" >&2; exit 1; }
import json, sys
r = json.load(open(sys.argv[1]))
if not r.get("ok"):
    sys.exit(f"bridge reset not ok: {str(r)[:400]}")
apps = {k: v for k, v in (r.get("apps") or {}).items() if v}
cart = (apps.get("shop") or {}).get("cart") or []
gift = sum(1 for l in cart if l.get("gift_message"))
ship = sum(1 for l in cart if l.get("ship_to_address_id"))
print(f"  ok · engine apps: {', '.join(sorted(apps))} · pushed: {', '.join(r.get('pushed') or []) or 'none'}")
print(f"  shop cart: {len(cart)} line(s) · {gift} gift message(s) · {ship} per-line ship-to")
PY

# ------------------------------------------------------ 5. annotator + URLs ---
# port_pids always exits 0 (it swallows lsof failures), so test reachability, not pids.
if ! up "http://127.0.0.1:$APP_PORT/index.html"; then
  detach "$PWD" "$LOGDIR/app.log" python3 -m http.server "$APP_PORT" --bind 127.0.0.1
  echo "annotator starting on $APP_PORT"
fi
wait_for "http://127.0.0.1:$APP_PORT/index.html" "annotator"

# The sids come back from /bridge/reset — they are the ones Bridge.push() actually
# wrote, so the URL opens the session the engine owns. ?bridge= is what puts the page
# in bridged mode; without it the mock would silently fall back to its local store.
"$PY" - "$LOGDIR/reset.json" "$MNUM" "$SEED" "$BRIDGE_URL" "$START_PATH" "$ROUTE_STYLE" \
      "http://127.0.0.1:$APP_PORT" <<'PY'
import json, sys, urllib.parse, urllib.request
reset_json, mnum, seed, bridge, start_path, style, app_url = sys.argv[1:8]
r = json.load(open(reset_json))
sids, mocks = r.get("sids") or {}, r.get("mocks") or {}

def route(app):
    """The step-0 page for an app. Only shop varies per task; the others have one
    landing page each, and anything without a route just opens at the app root."""
    if app == "shop":
        return start_path or "/"
    return {"mail": "/inbox", "market": "/", "calendar": "/", "food": "/"}.get(app, "/")


def url_for(app, sid, base, form):
    q = urllib.parse.urlencode({"sid": sid, "bridge": bridge})
    r = route(app)
    if not r or r == "/":
        return f"{base}/?{q}"
    if form == "hash":
        return f"{base}/?{q}#{r}"
    if form == "path":
        return f"{base}{r}?{q}"
    return f"{base}{r}?{q}#{r}"        # dual: whichever router the mock uses, it hits


def serves_shell(base, r):
    """Does the dev server return the SPA shell at this deep path?

    A wrong deep link does not error — it quietly lands on the mock's home page,
    which is exactly how the earlier hash-only guess went unnoticed. Vite's SPA
    fallback normally serves index.html for any path; if it does not, the path form
    is unusable and we drop back to hash-only for that app.
    """
    try:
        with urllib.request.urlopen(f"{base}{r}", timeout=5) as resp:
            return resp.status == 200 and 'id="root"' in resp.read(4096).decode("utf-8", "replace")
    except Exception:
        return False


apps = {}
for app, sid in sids.items():
    base = (mocks.get(app) or "").rstrip("/")
    if not base:
        continue
    r = route(app)
    form = style
    if style == "dual" and r and r != "/" and not serves_shell(base, r):
        print(f"  !! {app}: {base}{r} does not serve the app shell — using hash-only")
        form = "hash"
    apps[app] = url_for(app, sid, base, form)

json.dump({"mnum": mnum, "task_id": r.get("task_id"), "seed": int(seed),
           "mode": "bridged", "bridge": bridge, "start_path": start_path,
           "route_style": style, "routes": {a: route(a) for a in apps},
           "sids": sids, "apps": apps},
          open("live_env.json", "w"), indent=2)
print()
print(f"  task        {mnum}  ({r.get('task_id')})  seed {seed}   start {start_path}")
print(f"  annotator   {app_url}/index.html")
for app, url in apps.items():
    print(f"  {app:<11} {url}")
if not apps:
    sys.exit("no app URLs — the bridge pushed to no mock (check CUA_HUB_URL_* / mock ports)")
PY

echo
echo "  tip         allow pop-ups for 127.0.0.1:$APP_PORT so the annotator's"
echo "              \"Open all\" opens every app in one click (browsers cap it at one"
echo "              pop-up per click otherwise, and you'll click once per app)"
echo
echo "  verdict     ./run_local.sh --verify        (the gym's real milestones)"
echo "  re-seed     ./run_local.sh <MNUM> <seed>"
echo "  status      ./run_local.sh --status"
echo "  stop        ./run_local.sh --stop"
echo "  logs        $LOGDIR/"
