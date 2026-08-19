from fastapi import FastAPI
import os
from contextlib import asynccontextmanager
from api.db import init_db
from api.chat.routing import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/api/chats", tags=["chats"])



env = os.environ["ENVIRONMENT"]
debug = os.environ["DEBUG"]

if not env:
    raise NotImplementedError("ENV is not set")

@app.get("/")
async def root():
    return {"message": "Hello World" , "name" : "Prasanna Kumar", "env" : env, "debug" : debug}


@app.get("/user")
async def get_current_user():
    return {"name" : "Prasanna Kumar M"}
