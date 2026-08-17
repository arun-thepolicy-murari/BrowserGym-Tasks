# No private image in this delivery

Public tip-locked hub. Root `environment/<image>/` omitted on purpose (Tencent §1: only required for private images).

## Harbor G0 / G1 / G2

From `tasks/n446_redirect_shipped_throw_missing_cushion/`:

```bash
LOGS=$(mktemp -d); bash solution/solve.sh && LOGS="$LOGS" bash tests/test.sh   # G1 → 1.0
LOGS=$(mktemp -d) && bash tests/test.sh                    # G2 → 0.0
```
