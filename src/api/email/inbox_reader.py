import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from .imap_parser import GmailImapParser

load_dotenv()


email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")

if not email_address or not email_password:
    raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be set in environment variables")


def read_inbox(hours_ago=24, unread_only=True, verbose=False):
    parser = GmailImapParser(
        email_address = str(email_address),
        app_password = str(email_password)
    )
    emails = parser.fetch_emails(hours=hours_ago, unread_only=unread_only)

    if verbose:
        for email in emails:
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['timestamp']}")
            print("---")
    return emails

# read_inbox(hours_ago=4, unread_only=True, verbose=True)