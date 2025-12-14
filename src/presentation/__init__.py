import logging
import fastapi
from fastapi import Depends, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
import abc
from typing import Any, Annotated
from enum import Enum
from PIL import Image
import io
from datetime import datetime
from pydantic import BaseModel
from error import Error

class PresentationLogger:
    def __init__(self):
        self.logger = logging.getLogger("presentation")

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

class PresentationRequest(BaseModel):
    pass

class PresentationJSONResponse(JSONResponse):
    def __init__(self, status: int, content: dict[str, Any]):
        super().__init__(content=content, status_code=status)


class PresentationImageResponse(StreamingResponse):
    def __init__(self, status: int, image: Image.Image):
        if image.format is None:
            raise PresentationImageResponseError
        img_buffer = io.BytesIO()
        image.save(img_buffer, format=image.format)
        img_buffer.seek(0)
        super().__init__(content=img_buffer,
                         media_type=f"image/{image.format.lower()}", status_code=status)

class PresentationBase:
    router_path: str
    methods: list[str]
    tags: list[str | Enum] | None = None
    summary: str | None = None
    description: str | None = None
    responses: dict[int | str, dict[str, Any]] | None = None

    def __init__(self, logger: PresentationLogger):
        self.logger = logger

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route(
            self.router_path,
            self._handle,
            methods=self.methods,
            tags=self.tags,
            summary=self.summary,
            description=self.description,
            responses=self.responses,
        )

    async def _handle(self, *args, **kwargs):
        try:
            return await self.handle(*args, **kwargs)
        except Error as e:
            self.logger.error(f"Error: route: {self.router_path}, method: {self.methods}, message: {e.message}")
            return PresentationJSONResponse(status=500, content={"message": "Internal server error"})
        except Exception as e:
            self.logger.error(f"Unexpected error: route: {self.router_path}, method: {self.methods}, error: {e}")
            return PresentationJSONResponse(status=500, content={"message": "Internal server error"})

    @abc.abstractmethod
    async def handle(self, *args, **kwargs) -> PresentationJSONResponse | PresentationImageResponse:
        pass

class PresentationImageResponseError(Exception):
    pass

PresentationTypeAuthorization = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]

class PresentationImage:
    async def __call__(self, image: UploadFile) -> Image.Image:
        content = await image.read()
        pil_image = Image.open(io.BytesIO(content))
        pil_image.load()
        if pil_image.format is None:
            raise PresentationImageResponseError(f"image format is None: {image.filename}")
        return pil_image

PresentationTypeImage = Annotated[Image.Image, Depends(PresentationImage())]

PresentationTypeDatetime = Annotated[datetime, Form(...)]
