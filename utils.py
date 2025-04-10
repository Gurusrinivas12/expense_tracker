import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_alert_email(category, month, remaining):
    msg = MIMEText(f"⚠️ Alert! Only ₹{remaining} left for {category} in {month}.")
    msg['Subject'] = 'Budget Alert Notification'
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = 'tharunmadhavb@gmail.com'

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
    except Exception as e:
        print(f"Email alert failed: {e}")
