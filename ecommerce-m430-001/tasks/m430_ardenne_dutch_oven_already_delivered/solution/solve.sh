#!/usr/bin/env bash
# Gold / oracle for m430/ardenne_dutch_oven_already_delivered: Tell Alice ORD-ARDENNE-4 is already delivered (mail room / Vassiliou). Do not buy a replacement.
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/agent"
python3 - <<'PY'
import json, os
from pathlib import Path
logs = Path(os.environ.get("LOGS", "/logs"))
(logs / "agent").mkdir(parents=True, exist_ok=True)
outcome = json.loads('{"email_to": "alice@shopgym.com", "email_body": "The Ardenne Dutch oven ORD-ARDENNE-4 is already delivered \\u2014 signed for and held with concierge R. Vassiliou in the 2nd-floor mail room. I did not order a replacement.", "told_delivered": true, "named_collection": true, "bought_replacement": false, "harbor_gold": true, "success": true}')
(logs / "agent" / "outcome.json").write_text(json.dumps(outcome, indent=2) + "\n")
print("oracle wrote", logs / "agent" / "outcome.json")
PY
