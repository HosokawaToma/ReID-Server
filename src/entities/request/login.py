from pydantic import BaseModel


class EntitiesRequestLogin(BaseModel):
    client_id: str
    password: str
