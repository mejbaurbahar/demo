import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email():
    # Configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mejbaurbahar@gmail.com"
    password = "nbue qkic eioj nvfi" # App Password
    
    # Recipient from environment or default
    receiver_email = os.getenv("RECEIVER_EMAIL", "mejbaurbahar@gmail.com")
    
    print(f"Attempting to send email to {receiver_email} using {sender_email}...")

    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"AI QA Agent <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = f"Automation Test Report - {os.getenv('JOB_STATUS', 'Completed')}"

    body = "The automation test execution has completed. Please find the detailed HTML report attached."
    msg.attach(MIMEText(body, 'plain'))

    # Attach report
    filename = "reports/report.html"
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        sys.exit(1)

    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=report.html")
            msg.attach(part)

        # Connect and send
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("Logging in...")
        server.login(sender_email, password)
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"FAILED to send email: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    send_email()
