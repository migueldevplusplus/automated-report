import smtplib
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime
from config import CONFIG


def send_weekly_report_email(zip_path: Path, periods: dict):
    week_start, week_end = periods["current"]

    if not all([CONFIG["email_from"], CONFIG["email_to"], CONFIG["email_password"]]):
        print("Error: Missing email configuration (check .env)")
        return

    msg = EmailMessage()
    msg['Subject'] = f"Weekly Sales Report - {week_start:%d/%m/%Y} to {week_end:%d/%m/%Y}"
    msg['From'] = CONFIG["email_from"]
    msg['To'] = CONFIG["email_to"]

    body_html = f"""
    <html>
    <body>
    <h2>Weekly Sales Report</h2>
    <p>Period: {week_start:%d/%m/%Y} – {week_end:%d/%m/%Y}</p>
    <p>Attached is the ZIP file containing the detailed Excel report.</p>
    <p>Best regards,<br>Your automated reporting system</p>
    </body>
    </html>
    """
    msg.add_alternative(body_html, subtype='html')

    # Attach ZIP
    with open(zip_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='zip',
            filename=zip_path.name
        )

    try:
        with smtplib.SMTP(CONFIG["smtp_server"], CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(CONFIG["email_from"], CONFIG["email_password"])
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")