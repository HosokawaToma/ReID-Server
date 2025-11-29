import logging
import fastapi
from fastapi import Depends, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import abc
from typing import Any, Annotated
from enum import Enum
from PIL import Image
import io
from datetime import datetime
from pydantic import BaseModel

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


class PresentationBase:
    @property
    @abc.abstractmethod
    def router_path(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def methods(self) -> list[str]:
        pass

    tags: list[str | Enum] | None = None
    summary: str | None = None
    description: str | None = None
    responses: dict[int | str, dict[str, Any]] | None = None

    def __init__(self, logger: PresentationLogger):
        self.logger = logger

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route(
            self.router_path,
            self.handle,
            methods=self.methods,
            tags=self.tags,
            summary=self.summary,
            description=self.description,
            responses=self.responses,
        )

    @abc.abstractmethod
    async def handle(self, *args, **kwargs) -> Any:
        pass

class PresentationRequest(BaseModel):
    pass

class PresentationResponse(JSONResponse):
    def __init__(self, status: int, content: dict[str, Any]):
        super().__init__(content=content, status_code=status)

PresentationTypeAuthorization = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]

class PresentationImage:
    async def __call__(self, image: UploadFile) -> Image.Image:
        content = await image.read()
        pil_image = Image.open(io.BytesIO(content))
        pil_image.load()
        return pil_image

PresentationTypeImage = Annotated[Image.Image, Depends(PresentationImage())]

PresentationTypeDatetime = Annotated[datetime, Form(...)]
