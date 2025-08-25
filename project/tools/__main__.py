from .fetch_alarms import fetch_recent_alerts
import json

if __name__ == "__main__":
    alerts = fetch_recent_alerts()
    print(json.dumps(alerts, indent=2))
