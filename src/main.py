from fastapi import FastAPI
import os

app = FastAPI()

env = os.environ["ENV"]
debug = os.environ["DEBUG"]

if not env:
    raise NotImplementedError("ENV is not set")

@app.get("/")
async def root():
    return {"message": "Hello World" , "name" : "Prasanna Kumar", "env" : env, "debug" : debug}


@app.get("/user")
async def get_current_user():
    return {"name" : "Prasanna Kumar M"}
