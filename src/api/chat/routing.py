from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import result
from sqlmodel import Session, select
from typing import List
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from ..db import get_session

router = APIRouter()


@router.get("/")
def chat_health():
    return {"message": "Hello World"}


@router.post("/create")
def chat_create_message(payload : ChatMessagePayload, session : Session = Depends(get_session)):

    data = payload.model_dump()
    print(data)

    obj = ChatMessage.model_validate(data)

    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj

@router.get("/recent", response_model = List[ChatMessageListItem])
def chat_list_messages(session : Session = Depends(get_session)):
    query = select(ChatMessage).order_by(ChatMessage.created_at.desc())
    results = session.exec(query).fetchall()[:10]
    return [ChatMessageListItem.model_validate(result) for result in results]

