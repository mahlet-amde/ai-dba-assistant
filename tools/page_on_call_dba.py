from strands.tools import tool
import os
import smtplib


from email.mime.text import MIMEText

@tool
def page_on_call_dba(alert_message: str, urgency: str = "critical") -> str:
    dba_email = os.getenv("ON_CALL_DBA_EMAIL")
    if not dba_email:
        raise ValueError("Missing ON_CALL_DBA_EMAIL in environment variables.")

    subject = f"[DBA PAGE] Urgent Alert - {urgency.upper()}"
    body = f"""An alert requires DBA attention.

Urgency: {urgency}
Alert: {alert_message}

Please respond via the DBA dashboard or notify the incident team.
""" 

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("NOTIFY_FROM_EMAIL", "noreply@alerts.ai")
    msg["To"] = dba_email

    try:
        with smtplib.SMTP("localhost") as server:
            server.sendmail(msg["From"], [dba_email], msg.as_string())
        return "Alert sent to DBA: {dba_email}"
    except Exception as e:
        return " Failed to page DBA: {e}"
