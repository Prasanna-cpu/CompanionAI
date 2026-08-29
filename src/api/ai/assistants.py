from .llms import get_openai_llm
from .schemas import EmailMessageSchema
from .tools import get_unread_emails, send_me_email

EMAIL_TOOLS = {
    "send_me_email" : send_me_email,
    "get_unread_emails" : get_unread_emails
}

def email_assistant(query:str):
    query_lower = query.lower()
    
    # Direct tool invocation based on query intent (fallback for models without function calling)
    if "send" in query_lower and "email" in query_lower:
        # Generate email content using LLM
        llm_base = get_openai_llm()
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Generate email content in plain text without markdown."},
            {"role": "user", "content": f"Generate an email about: {query}"}
        ]
        response = llm_base.invoke(messages)
        content = response.content
        
        # Extract subject and body
        lines = content.split('\n')
        subject = lines[0].replace('Subject:', '').strip() if 'Subject:' in lines[0] else "Generated Email"
        body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content
        
        # Send the email
        result = send_me_email.invoke({"subject": subject, "content": body})
        return f"Email sent: {result}\n\nGenerated content:\n{content}"
    
    elif "unread" in query_lower or "get" in query_lower and "email" in query_lower:
        # Get unread emails
        result = get_unread_emails.invoke({"hours_ago": 6})
        return f"Unread emails:\n{result}"
    
    else:
        # General query - just use LLM
        llm_base = get_openai_llm()
        messages = [
            {"role": "system", "content": "You are a helpful assistant that can help you with your emails."},
            {"role": "user", "content": f"{query} do not use markdown , use only plaintext"}
        ]
        response = llm_base.invoke(messages)
        return response.content

print(email_assistant("Send me an email about 4 points about 2026 Jantar Mantar Protests"))