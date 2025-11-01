from pydantic import BaseModel


class PresentationRtcOfferRequest(BaseModel):
    sdp: str
    type: str
