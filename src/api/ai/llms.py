import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL_NAME")
openai_base_url = os.environ.get("OPENAI_BASE_URL")

# print(f"OPENAI_BASE_URL: {openai_base_url}")
# print(f"OPENAI_MODEL_NAME: {openai_model}")

if not openai_api_key or not openai_model or not openai_base_url:
    raise ValueError("OPENAI_API_KEY, OPENAI_MODEL, and OPENAI_BASE_URL are required")

def get_openai_llm():
    open_api_params = {
        "model": openai_model,
        "base_url": openai_base_url,
        "api_key": openai_api_key,
        "max_tokens": 512,
        "temperature": 0.3,
        "streaming": True
    }

    llm_base = ChatOpenAI(**open_api_params)
    return llm_base

def get_openai_llm_direct():
    """Use OpenAI's actual API for testing tool calling"""
    import os
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0.3,
        base_url="https://api.openai.com/v1"  # Explicitly use OpenAI's API
    )