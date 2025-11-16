from pydantic import BaseModel
from datetime import datetime


class PresentationPersonPathRequest(BaseModel):
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
