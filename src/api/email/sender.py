from email.message import EmailMessage
import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")

# print(f"EMAIL_ADDRESS: {email_address}")
# print(f"EMAIL_PASSWORD: {email_password}")

if not email_address or not email_password:
    raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD are required")

email_host = os.environ.get("EMAIL_HOST")
email_port = os.environ.get("EMAIL_PORT")

if not email_host or not email_port:
    raise ValueError("EMAIL_HOST and EMAIL_PORT are required")

email_host = str(email_host)
email_port = int(email_port)

def send_mail(
        subject : str = "No Subject Provided",
        content : str = "No Message Provided",
        to_email : str = email_address,
        from_email : str = email_address
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(content)

    with smtplib.SMTP_SSL(email_host, email_port) as smtp:
        smtp.login(email_address, email_password)
        return smtp.send_message(msg)



