#!/usr/bin/env bash
# Gold / oracle for ui_041/wiper_blades_ask_size: Read 27 Aug car service; ask Alice the blade size; buy nothing.
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/agent"
python3 - <<'PY'
import json, os
from pathlib import Path
logs = Path(os.environ.get("LOGS", "/logs"))
(logs / "agent").mkdir(parents=True, exist_ok=True)
outcome = json.loads('{"email_to": "alice@shopgym.com", "email_body": "Car service is Thu 27 Aug. No wiper size is on the account or in mail. What size should I order? I have not bought blades.", "asked_size": true, "bought": false, "read_calendar": true, "harbor_gold": true, "success": true}')
(logs / "agent" / "outcome.json").write_text(json.dumps(outcome, indent=2) + "\n")
print("oracle wrote", logs / "agent" / "outcome.json")
PY
