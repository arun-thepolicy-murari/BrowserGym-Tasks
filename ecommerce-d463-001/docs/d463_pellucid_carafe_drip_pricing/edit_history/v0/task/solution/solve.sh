#!/usr/bin/env bash
# Gold / oracle for d463/pellucid_carafe_drip_pricing: Buy ValueMart first-party carafe $56. Email Alice the all-in comparison including ShopGym glass $8.50 + signature $5.99 (sticker $49 is not all-in).
set -euo pipefail
LOGS="${LOGS:-/logs}"
mkdir -p "$LOGS/agent"
python3 - <<'PY'
import json, os
from pathlib import Path
logs = Path(os.environ.get("LOGS", "/logs"))
(logs / "agent").mkdir(parents=True, exist_ok=True)
outcome = json.loads('{"email_to": "alice@shopgym.com", "email_body": "Bought ValueMart first-party Pellucid carafe $56.00. ShopGym $49 sticker is $63.49 all-in after glass shipping $8.50 and signature $5.99. GlassHaul marketplace is worse after oversized + signature.", "bought_vm_56": true, "mentioned_6349_or_fees": true, "bought_shopgym": false, "harbor_gold": true, "success": true}')
(logs / "agent" / "outcome.json").write_text(json.dumps(outcome, indent=2) + "\n")
print("oracle wrote", logs / "agent" / "outcome.json")
PY
