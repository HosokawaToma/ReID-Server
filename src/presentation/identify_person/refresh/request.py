from datetime import datetime
from pydantic import BaseModel


class PresentationIdentifyPersonRefreshRequest(BaseModel):
    after_timestamp: datetime | None
    before_timestamp: datetime | None
    camera_ids: list[int] | None
    view_ids: list[int] | None



