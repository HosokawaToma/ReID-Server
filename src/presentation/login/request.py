from pydantic import BaseModel

class PresentationLoginRequest(BaseModel):
    client_id: str
    password: str
