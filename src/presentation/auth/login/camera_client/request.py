from pydantic import BaseModel

class PresentationAuthLoginCameraClientRequest(BaseModel):
    camera_client_id: str
    password: str
