from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from dto.image import DtoImage
import io
from typing import Any

class PresentationUtilJSONResponse(JSONResponse):
    REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24  # 1 day

    def __init__(self, status: int, content: dict[str, Any]):
        super().__init__(content=content, status_code=status)

    def set_refresh_token(self, refresh_token: str):
        self.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=self.REFRESH_TOKEN_MAX_AGE,
            path="/",
            secure=True,
            httponly=True,
            samesite="strict",
        )


class PresentationUtilImageResponse(StreamingResponse):
    def __init__(self, status: int, image: DtoImage):
        super().__init__(
            content=io.BytesIO(image.bytes),
            media_type=f"image/{image.format.lower()}",
            status_code=status,
        )
