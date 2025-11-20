from pydantic import BaseModel

class PresentationAdminClientAuthLoginCredentialRequest(BaseModel):
    id: str
    password: str
