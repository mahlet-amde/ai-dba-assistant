# Testing Notes
---

## Recent Alerts (DB) — Stub Mode
You do not need Postgres to test. The tool `project/tools/fetch_alarms.py` now works in two modes:

- **Stub mode (default):** If `ENABLE_ALERTS_STUB=true` OR Postgres env vars are missing,
  it returns sample alerts from `sample_data/recent_alerts.json`.


Example (stub mode):
```bash
export ENABLE_ALERTS_STUB=true
python -m project.main
```


## Quick CLI test for recent alerts tool

You can now run the tool directly (without launching the whole project):

```bash
python -m project.tools
```

This will print either:
- Sample alerts from `sample_data/recent_alerts.json` (stub mode), OR
- Live alerts from Postgres (if DB vars are set).
