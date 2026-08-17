#!/usr/bin/env bash
# Gold / oracle for ui_052/jacket_return_reorder_large: Read Northgate fit note; start return on ORD-JACKET-441 Medium; buy Large via variant picker (not Buy Again).
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/agent"
python3 - <<'PY'
import json, os
from pathlib import Path
logs = Path(os.environ.get("LOGS", "/logs"))
(logs / "agent").mkdir(parents=True, exist_ok=True)
outcome = json.loads('{"email_to": "alice@shopgym.com", "email_body": "Started the Medium return on ORD-JACKET-441 and ordered Large from the variant picker. Did not Buy Again.", "returned_medium": true, "bought_large": true, "rebought_medium": false, "harbor_gold": true, "success": true}')
(logs / "agent" / "outcome.json").write_text(json.dumps(outcome, indent=2) + "\n")
print("oracle wrote", logs / "agent" / "outcome.json")
PY
