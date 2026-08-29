from langchain_core.tools import tool
from packaging import metadata

from .services import generate_email_message
from ..email.sender import send_mail
from ..email.inbox_reader import read_inbox
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool


@tool
def research_email(query : str, config : RunnableConfig):
    """Perform Research Bases on Query"""
    metadata = config.get("metadata")
    add_field = metadata.get("additional_field")
    print(f"research_email called with query: {query}, metadata: {metadata}, additional_field: {add_field}")
    response = generate_email_message(query)
    msg = f"Subject {response.subject} : \n Body : {response.body}"
    return msg


@tool
def send_me_email(subject : str, content : str):
    """Send an email with the given subject and content."""
    try:
        send_mail(subject = subject, content = content)
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
    finally:
        print(f"send_me_email called with subject: {subject}, content: {content}")


@tool
def get_unread_emails(hours_ago : int = 6):
    """Get unread emails from the past specified number of hours."""
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=True)
        cleaned = []
        for email in emails:
            data = email.copy()
            if "html_body" in data:
                data.pop('html_body')
            msg = ""
            for k, v in data.items():
                msg += f"{k}:	{v}"
            cleaned.append(msg)
        return "\n-----\n".join(cleaned)[:500]
    except Exception as e:
        return f"Failed to get unread emails: {str(e)}"
    finally:
        print(f"get_unread_emails called with hours_ago: {hours_ago}")
