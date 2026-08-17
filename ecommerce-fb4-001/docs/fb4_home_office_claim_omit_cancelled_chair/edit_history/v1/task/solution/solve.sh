#!/usr/bin/env bash
# Gold / oracle for fb4/home_office_claim_omit_cancelled_chair: Verify ORD-CHAIR-17 still charged/delivered; include $329 chair; email Alice line items totaling $810.49; do not email Sydney; $0 new spend.
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/agent"
python3 - <<'PY'
import json, os
from pathlib import Path
logs = Path(os.environ.get("LOGS", "/logs"))
(logs / "agent").mkdir(parents=True, exist_ok=True)
outcome = json.loads('{"email_to": "alice@shopgym.com", "email_body": "Desk $249.00 ORD-DESK-11, monitor $189.99 ORD-MON-13, lamp $42.50 ORD-LAMP-15, chair $329.00 ORD-CHAIR-17 still charged (cancel email is wrong). Total $810.49. Hoodie is personal, omitted. I emailed you not Sydney.", "total": 810.49, "included_chair": true, "emailed_sydney": false, "new_orders": false, "harbor_gold": true, "success": true}')
(logs / "agent" / "outcome.json").write_text(json.dumps(outcome, indent=2) + "\n")
print("oracle wrote", logs / "agent" / "outcome.json")
PY
