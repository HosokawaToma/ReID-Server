from pydantic import BaseModel


class PresentationCameraClientsCreateRequest(BaseModel):
    camera_client_id: str
    password: str
    camera_id: int
    view_id: int
