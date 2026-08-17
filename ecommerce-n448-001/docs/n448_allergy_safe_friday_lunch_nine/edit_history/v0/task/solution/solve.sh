#!/usr/bin/env bash
# Gold / oracle for n448/allergy_safe_friday_lunch_nine: Saltbox $99.49 for 9 (not Vesuvio pesto); ValueMart plates/cups SKU $23.73; omit water to hold $125; email Alice with veto/allergy/totals.
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/agent"
python3 - <<'PY'
import json, os
from pathlib import Path
logs = Path(os.environ.get("LOGS", "/logs"))
(logs / "agent").mkdir(parents=True, exist_ok=True)
outcome = json.loads('{"email_to": "alice@shopgym.com", "email_body": "Saltbox FOOD-1041 $99.49 for nine. Skipped Vesuvio because Marcus veto + nut/pesto allergy on the calendar. Bought ValueMart plates/cups $23.73. Omitted fizzy water to stay under $125. Total $123.22.", "saltbox": true, "plates_sku": true, "vesuvio": false, "over_cap": false, "harbor_gold": true, "success": true}')
(logs / "agent" / "outcome.json").write_text(json.dumps(outcome, indent=2) + "\n")
print("oracle wrote", logs / "agent" / "outcome.json")
PY
