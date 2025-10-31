from pydantic import BaseModel

class PresentationLoginCameraClientRequest(BaseModel):
    camera_client_id: str
    password: str
