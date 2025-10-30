from pydantic import BaseModel


class PresentationRtcRequest(BaseModel):
    sdp: str
    type: str
