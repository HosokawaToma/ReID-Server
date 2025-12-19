import logging
import fastapi
from fastapi import Depends, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
import abc
from functools import lru_cache
from typing import Any, Annotated, Sequence
from enum import Enum
from PIL import Image
import io
from datetime import datetime
from fastapi import Request
from applications.admin_client.auth.oauth2 import ApplicationAdminClientAuthOAuth2
from applications.admin_client.auth.oauth2 import ApplicationAdminClientAuthOAuth2Params
from applications.admin_client.auth.oauth2 import ApplicationAdminClientAuthOAuth2Error
from environment import Environment
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

class PresentationRequest(Request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_refresh_token(self) -> str:
        return self.cookies.get("refresh_token", "")

class PresentationRequestBody(BaseModel):
    pass

class PresentationJSONResponse(JSONResponse):
    REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24 # 1 day

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

class PresentationImageResponseError(Exception):
    pass

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
    dependencies: Sequence[Annotated[Any, Depends]] | None = None

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
            dependencies=self.dependencies,
        )

    @abc.abstractmethod
    async def handle(self, *args, **kwargs) -> PresentationJSONResponse | PresentationImageResponse:
        pass

PresentationTypeAuthorization = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]

@lru_cache
def get_admin_client_auth_application(
    environment: Environment = Depends(Environment)
) -> ApplicationAdminClientAuthOAuth2:
    return ApplicationAdminClientAuthOAuth2.create(environment)

def admin_client_authenticated(
    token: PresentationTypeAuthorization,
    application: ApplicationAdminClientAuthOAuth2 = Depends(get_admin_client_auth_application),
) -> str:
    try:
        result = application.oauth2(ApplicationAdminClientAuthOAuth2Params(token=token))
    except ApplicationAdminClientAuthOAuth2Error as error:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result.admin_client_id

PresentationAdminClientAuthenticated = Annotated[str, Depends(admin_client_authenticated)]


class PresentationImageError(Exception):
    pass

class PresentationImage:
    async def __call__(self, image: UploadFile) -> Image.Image:
        content = await image.read()
        pil_image = Image.open(io.BytesIO(content))
        pil_image.load()
        if pil_image.format is None:
            raise PresentationImageError(f"image format is None: {image.filename}")
        return pil_image

PresentationTypeImage = Annotated[Image.Image, Depends(PresentationImage())]

PresentationTypeDatetime = Annotated[datetime, Form(...)]

PresentationTypeInt = Annotated[int, Form(...)]
