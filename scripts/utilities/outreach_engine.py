from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


class SaaSOutreachEngine:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def build_message(self, to_email, first_name, vector_data):
        if vector_data.get("vector_type") == "REAL_ESTATE_FIRE_SALE":
            subject = f"Property signal update for {vector_data.get('target_region', 'your market')}"
            body = (
                f"Hi {first_name},\n\n"
                f"I found a signal in {vector_data.get('target_region', 'your market')}: "
                f"{vector_data.get('signal', 'no details provided')}.\n\n"
                f"If you want the underlying data in a cleaner format, I can package it.\n\n"
                f"Best,\nSaaS Outreach Engine"
            )
        else:
            subject = f"Market signal update for {vector_data.get('target_region', 'your market')}"
            body = (
                f"Hi {first_name},\n\n"
                f"I found a notable signal for {vector_data.get('target_region', 'your market')}: "
                f"{vector_data.get('signal', 'no details provided')}.\n\n"
                f"If you want the structured data, I can package it for review.\n\n"
                f"Best,\nSaaS Outreach Engine"
            )

        msg = EmailMessage()
        msg["From"] = self.sender_email or ""
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)
        return msg

    def send_automated_pitch(self, to_email, first_name, vector_data, allow_send=False):
        if not self.sender_email or not self.sender_password:
            print("email credentials missing; returning draft only")
            return self.build_message(to_email, first_name, vector_data)

        msg = self.build_message(to_email, first_name, vector_data)
        if not allow_send:
            return msg

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print(f"sent pitch to {first_name} <{to_email}>")
            return True
        except Exception as exc:
            print(f"failed to transmit email to {to_email}: {exc}")
            return False


if __name__ == "__main__":
    print("testing outreach engine...")
    engine = SaaSOutreachEngine()
    mock_targets = [
        {
            "email": "local_flipper_lead@example.com",
            "name": "Mike",
            "vector_type": "REAL_ESTATE_FIRE_SALE",
            "target_region": "Metro Atlanta, GA",
            "signal": "Spike in pre-foreclosures.",
        },
        {
            "email": "fund_manager_lead@example.com",
            "name": "Sarah",
            "vector_type": "EQUITY_CAPITULATION",
            "target_region": "Commercial REIT Sector",
            "signal": "Heavy outflows and elevated put volume.",
        },
    ]

    for target in mock_targets:
        draft = engine.send_automated_pitch(target["email"], target["name"], target)
        print(draft)
