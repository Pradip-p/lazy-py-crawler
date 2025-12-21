import aiosmtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
import logging

logger = logging.getLogger(__name__)

# Email Configuration from environment
EMAIL_HOST = os.getenv("EMAIL_HOST", "email-smtp.ap-south-1.amazonaws.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT") or os.getenv("SMTP_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAILS_FROM_NAME = os.getenv("EMAILS_FROM_NAME", "Lazy Crawler Support")
EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL") or EMAIL_HOST_USER
CONTACT_RECIPIENT_EMAIL = os.getenv("CONTACT_RECIPIENT_EMAIL")


async def send_contact_email(full_name: str, email: str, message: str):
    """
    Sends an email notification for a contact form submission.
    Follows the reference structure using aiosmtplib and MIMEText.
    """
    missing = [
        name
        for name, val in {
            "EMAIL_HOST": EMAIL_HOST,
            "EMAIL_HOST_USER": EMAIL_HOST_USER,
            "EMAIL_HOST_PASSWORD": EMAIL_HOST_PASSWORD,
            "EMAILS_FROM_EMAIL": EMAILS_FROM_EMAIL,
            "CONTACT_RECIPIENT_EMAIL": CONTACT_RECIPIENT_EMAIL,
        }.items()
        if not val
    ]

    if missing:
        logger.warning(
            f"Email configurations are missing: {', '.join(missing)}. Cannot send email."
        )
        return

    subject = f"New Contact Form Submission: {full_name}"
    formatted_message = message.replace("\n", "<br>")
    html_content = f"""
    <html>
        <body>
            <h2 style="color: #611f69;">New Contact Form Submission</h2>
            <p><strong>Full Name:</strong> {full_name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong></p>
            <div style="background: #f8f8f8; padding: 15px; border-radius: 5px; border: 1px solid #ddd;">
                {formatted_message}
            </div>
            <hr style="border: none; border-top: 1px solid #eee; margin-top: 20px;">
            <p style="font-size: 0.8rem; color: #888;">Sent from Lazy Crawler Notification System</p>
        </body>
    </html>
    """

    message_obj = MIMEText(html_content, "html")
    message_obj["Subject"] = subject
    message_obj["From"] = formataddr((EMAILS_FROM_NAME, EMAILS_FROM_EMAIL))
    message_obj["To"] = CONTACT_RECIPIENT_EMAIL

    try:
        logger.debug(
            f"Sending email from {EMAILS_FROM_EMAIL} to {CONTACT_RECIPIENT_EMAIL}"
        )
        await aiosmtplib.send(
            message_obj,
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL_HOST_USER,
            password=EMAIL_HOST_PASSWORD,
            use_tls=False if EMAIL_PORT == 587 else True,
            start_tls=True if EMAIL_PORT == 587 else False,
        )
        logger.info(f"Email sent successfully to {CONTACT_RECIPIENT_EMAIL}")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
