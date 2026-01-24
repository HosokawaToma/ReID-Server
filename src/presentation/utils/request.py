from fastapi import Request
from pydantic import BaseModel


class PresentationUtilRequest(Request):
    UNKNOWN_REQUEST_ID = "unknown"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_refresh_token(self) -> str:
        return self.cookies.get("refresh_token", "")

    def get_request_id(self) -> str:
        if self.state is not None:
            return getattr(self.state, "request_id", self.UNKNOWN_REQUEST_ID)
        else:
            return self.UNKNOWN_REQUEST_ID


class PresentationUtilRequestBody(BaseModel):
    pass
