#!/usr/bin/env bash
# Gold / oracle for fb5/jason_desk_kit_samantha_cap: ValueMart Flow mat + notebooks + pens + VALUE10 Friday AM; Sakura lunch; email Alice store charges. Do not keep the ShopGym Sunday mat.
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/agent"
python3 - <<'PY'
import json, os
from pathlib import Path
logs = Path(os.environ.get("LOGS", "/logs"))
(logs / "agent").mkdir(parents=True, exist_ok=True)
outcome = json.loads('{"email_to": "alice@shopgym.com", "email_body": "ValueMart Flow mat + notebooks + pens with VALUE10 $60.30 Friday 9:00. Sakura $51.49. All-in $111.79, inside Samantha $120. Did not buy the ShopGym mat (Sunday / worse delivered).", "vm_kit": true, "coupon": true, "sakura": true, "shopgym_mat_kept": false, "harbor_gold": true, "success": true}')
(logs / "agent" / "outcome.json").write_text(json.dumps(outcome, indent=2) + "\n")
print("oracle wrote", logs / "agent" / "outcome.json")
PY
