from pydantic import BaseModel


class PresentationLoginAdminClientRequest(BaseModel):
    admin_client_id: str
    password: str
