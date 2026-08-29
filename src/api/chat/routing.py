from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
import time
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from ..db import get_session
from ..ai.services import generate_email_message
from src.api.ai.schemas import EmailMessageSchema, SupervisorSchema
from ..ai.agents import get_supervisor
from fastapi import HTTPException
from langchain_openai.chat_models.base import OpenAIAPIError

router = APIRouter()


@router.get("/")
def chat_health():
    return {"message": "Hello World"}


@router.post("/create", response_model = SupervisorSchema)
async def chat_create_message(payload : ChatMessagePayload, session : Session = Depends(get_session)):

    data = payload.model_dump()
    print(data)

    obj = ChatMessage.model_validate(data)

    session.add(obj)
    session.commit()
    # session.refresh(obj)
    #
    # response = generate_email_message(payload.message)
    #
    # return response
    supervisor = get_supervisor()
    msg_data = {
        "messages" : [
            {
                "role" : "user",
                "content" : f"{payload.message}"
            }
        ]
    }
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            result = supervisor.invoke(msg_data)
            break
        except OpenAIAPIError as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            raise HTTPException(status_code=503, detail=f"OpenAI API server error (GPU memory exhausted): {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating message: {str(e)}")
    if not result:
        raise HTTPException(status_code = 500, detail = "Failed to generate email message")
    messages = result.get("messages", [])
    if not messages:
        raise HTTPException(status_code = 500, detail = "Failed to generate email message")
    last_message = messages[-1]
    return SupervisorSchema(content=str(last_message.content))

@router.get("/recent", response_model = List[ChatMessageListItem])
def chat_list_messages(session : Session = Depends(get_session)):
    query = select(ChatMessage).order_by(ChatMessage.created_at.desc())
    results = session.exec(query).fetchall()[:10]
    return [ChatMessageListItem.model_validate(result) for result in results]

