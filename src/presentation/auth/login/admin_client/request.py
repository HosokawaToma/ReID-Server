from pydantic import BaseModel


class PresentationAuthLoginAdminClientRequest(BaseModel):
    admin_client_id: str
    password: str
