#!/usr/bin/env python3
"""Automate outreach to businesses without websites."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv

def send_email(sender_email, sender_password, recipient_email, subject, body):
    """Send an email using SMTP."""
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

def automate_outreach(csv_file, sender_email, sender_password):
    """Automate outreach to businesses listed in the CSV file."""
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            business_name = row["name"]
            business_email = f"contact@{business_name.replace(' ', '').lower()}.com"  # Placeholder
            
            subject = f"Enhance Your Online Presence with a Custom Website"
            body = f"""
Dear {business_name},

We noticed that your business has excellent reviews but lacks a website. A custom website can help you attract more customers and grow your business.

We specialize in creating slick, minimalist websites with integrated AI chatbot wrappers to enhance customer engagement. Let us help you establish a strong online presence.

Best regards,
Vertical AI Team
"""
            
            send_email(sender_email, sender_password, business_email, subject, body)

def main():
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your password
    csv_file = "businesses_without_websites.csv"
    
    print(f"Starting automated outreach to businesses listed in {csv_file}...")
    automate_outreach(csv_file, sender_email, sender_password)
    print("Outreach completed.")

if __name__ == "__main__":
    main()
