import os
import logging
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP, SMTPException

# Load environment variables
load_dotenv()
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Async function to send email
async def send_email(to_email, subject, body):
    if not all([GMAIL_USER, GMAIL_PASSWORD]):
        logger.error("Missing GMAIL_USER or GMAIL_PASSWORD in environment variables.")
        return False

    try:
        # Prepare the email
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email
        smtp = SMTP(hostname="smtp.gmail.com", port=587, start_tls=True)
        await smtp.connect()
        await smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        await smtp.send_message(msg)
        await smtp.quit()

        logger.info(f"✅ Email sent successfully to {to_email}")
        return True

    except SMTPException as smtp_err:
        logger.error(f"SMTP error: {smtp_err}")
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
    return False
