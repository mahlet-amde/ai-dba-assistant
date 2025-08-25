import os, json, datetime
from typing import List, Dict, Any

# Optional Postgres mode (if you add psycopg / creds later)
try:
    import psycopg  # psycopg3
except Exception:
    psycopg = None

SAMPLE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_data", "recent_alerts.json")

def _load_stub() -> List[Dict[str, Any]]:
    # Load from sample_data/recent_alerts.json or return a default set
    try:
        with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Fallback defaults
        now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        return [
            {"id": 1, "created_at": now, "severity": "CRITICAL", "message": "Replication lag > 900s on db-prod-2", "host": "db-prod-2"},
            {"id": 2, "created_at": now, "severity": "WARNING", "message": "High connections on api-gateway", "host": "api-gateway"},
        ]

def _should_use_stub() -> bool:
    # Use stub if explicitly enabled OR if required DB env vars are missing
    enable = os.getenv("ENABLE_ALERTS_STUB", "").lower() in ("1", "true", "yes")
    required = ["PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    return enable or len(missing) > 0 or psycopg is None

def fetch_recent_alerts(limit: int = 10, since_minutes: int = 1440) -> List[Dict[str, Any]]:
    """Return recent alerts.
    - Stub mode: returns sample alerts from JSON.
    - Postgres mode: queries alerts table (requires psycopg + env vars).
    """
    if _should_use_stub():
        alerts = _load_stub()
        # Sort newest first and slice
        alerts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return alerts[:limit]

    # Real Postgres path (optional)
    conn_kwargs = dict(
        host=os.getenv("PGHOST"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=int(os.getenv("PGPORT", "5432")),
    )
    query = f"""
        SELECT id, created_at, severity, message, host
        FROM alerts
        WHERE created_at >= NOW() - INTERVAL '{since_minutes} minutes'
        ORDER BY created_at DESC
        LIMIT {limit};
    """
    with psycopg.connect(**conn_kwargs) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            cols = [c[0] for c in cur.description]
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    return rows

# Simple tool interface expected by the agent system
class RecentAlertsTool:
    name = "recent_alerts"
    description = "Fetch recent alerts from Postgres or stubbed sample data if DB is not configured."

    def __call__(self, query=None):
        limit = 10
        since = 1440
        if isinstance(query, dict):
            limit = int(query.get("limit", limit))
            since = int(query.get("since_minutes", since))
        return fetch_recent_alerts(limit=limit, since_minutes=since)
