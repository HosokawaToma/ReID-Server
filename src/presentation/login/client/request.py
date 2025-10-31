from pydantic import BaseModel


class PresentationLoginClientRequest(BaseModel):
    client_id: str
    password: str
