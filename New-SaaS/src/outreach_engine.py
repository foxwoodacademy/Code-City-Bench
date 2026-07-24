import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SaaSOutreachEngine:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_automated_pitch(self, to_email, first_name, vector_data):
        """Builds and fires the customized high-velocity pitch email."""
        if not self.sender_email or not self.sender_password:
            print("⚠️ Email credentials missing in .env. Skipping actual transmission.")
            return False

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email

        # Dynamic template selection based on asset type
        if vector_data['vector_type'] == 'REAL_ESTATE_FIRE_SALE':
            msg['Subject'] = f"Distressed Lead Telemetry: {vector_data['target_region']} Fire-Sales (Off-Market)"
            body = (
                f"Hey {first_name},\n\n"
                f"Our property data engine just flagged a critical anomaly in the {vector_data['target_region']} sub-market: "
                f"{vector_data['signal']}\n\n"
                f"These are fatigued owners and distressed assets that haven't hit Zillow or the MLS yet. "
                f"They are prime targets for all-cash, fast-close offers at 60% ARV.\n\n"
                f"We have compiled the raw text data blocks directly for local cash-buyers to feed straight into "
                f"their systems tonight. Let me know if I should drop the file on your desk.\n\n"
                f"Best,\nSaaS Acquisition Engine"
            )
        else:
            msg['Subject'] = f"Structural Capitulation Warning: {vector_data['target_region']} Liquidity Signal"
            body = (
                f"{first_name},\n\n"
                f"Our institutional risk telemetry platform just picked up a significant velocity anomaly regarding "
                f"the {vector_data['target_region']}: {vector_data['signal']}\n\n"
                f"Retail sentiment hasn't priced this in yet, but the institutional liquidity exit has begun. "
                f"We are routing structured raw JSON feeds of these panic-vectors to select funds before the opening bell.\n\n"
                f"If your desk is exposed, I can open an active API endpoint for your team tonight. Let me know.\n\n"
                f"Best,\nSaaS Risk Architecture Lead"
            )

        msg.attach(MIMEText(body, 'plain'))

        try:
            # Secure SMTP connection sequence
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_mail(self.sender_email, to_email, msg.as_string())
            server.quit()
            print(f"📧 [EMAIL SENT] Pitch successfully dispatched to {first_name} ({to_email})")
            return True
        except Exception as e:
            print(f"❌ Failed to transmit email to {to_email}: {e}")
            return False

if __name__ == "__main__":
    # Test execution with mock endpoints
    print("Testing Outreach Engine...")
    engine = SaaSOutreachEngine()
    
    # Mocking sample endpoint targets for tonight
    mock_targets = [
        {"email": "local_flipper_lead@example.com", "name": "Mike", "vector_type": "REAL_ESTATE_FIRE_SALE", "target_region": "Metro Atlanta, GA", "signal": "Sudden 34% spike in pre-foreclosures."},
        {"email": "fund_manager_lead@example.com", "name": "Sarah", "vector_type": "EQUITY_CAPITULATION", "target_region": "Commercial REIT Sector", "signal": "Insiders dumped 45% of holdings."}
    ]
    
    for target in mock_targets:
        engine.send_automated_pitch(target['email'], target['name'], target)
