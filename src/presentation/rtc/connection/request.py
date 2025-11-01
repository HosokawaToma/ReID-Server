from pydantic import BaseModel


class PresentationRtcConnectionRequest(BaseModel):
    sdp: str
    type: str
