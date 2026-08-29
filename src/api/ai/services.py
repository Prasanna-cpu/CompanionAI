from src.api.ai.llms import get_openai_llm
from src.api.ai.schemas import EmailMessageSchema
import json
import re


def generate_email_message(query : str):
    llm_base = get_openai_llm()
    messages = [
        ("system", "You are a helpful assistant. Always respond in valid JSON format with 'subject' and 'body' fields. Do not use markdown."),
        ("human", f"{query}")
    ]
    response = llm_base.invoke(messages)
    
    # Parse JSON from response
    content = response.content
    try:
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            return EmailMessageSchema(**data)
        else:
            # Fallback if no JSON found
            return EmailMessageSchema(
                subject="Generated Email",
                body=content,
                invalid_request=True
            )
    except Exception as e:
        # Fallback on parsing error
        return EmailMessageSchema(
            subject="Generated Email",
            body=content,
            invalid_request=True
        )


