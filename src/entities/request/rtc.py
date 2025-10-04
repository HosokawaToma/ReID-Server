from pydantic import BaseModel


class EntitiesRequestRtc(BaseModel):
    sdp: str
    type: str
