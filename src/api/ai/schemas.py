from pydantic import BaseModel, Field

class EmailMessageSchema(BaseModel):
    subject : str
    body : str
    invalid_request : bool | None = Field(default = False)

class SupervisorSchema(BaseModel):
    content : str