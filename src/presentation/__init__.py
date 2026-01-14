import fastapi
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Depends, UploadFile, Form, HTTPException, Path
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
import abc
from typing import Any, Annotated, Sequence, Callable, Awaitable, Type, TypeVar, Generic
from enum import Enum
from PIL import Image
import io
from datetime import datetime
from fastapi import Request, Response
from applications.admin_client.auth.oauth2 import ApplicationAdminClientAuthOAuth2
from applications.admin_client.auth.oauth2 import ApplicationAdminClientAuthOAuth2Error
from dto.admin_client.auth.token import DtoAdminClientAuthToken
from dto.admin_client.id import DtoAdminClientId
from environment import Environment
from pydantic import BaseModel
from error import Error
import uuid
from logger import Logger
import asyncio
from applications import ApplicationBase


class PresentationRequest(Request):
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


class PresentationRequestBody(BaseModel):
    pass


class PresentationJSONResponse(JSONResponse):
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

    def __init__(self, logger: Logger):
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


class PresentationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, logger: Logger):
        super().__init__(app=app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        self.logger.api_request_info(request_id=request_id, request_path=request.url.path, request_method=request.method)
        response = await call_next(request)
        self.logger.api_response_info(request_id=request_id, response_status_code=response.status_code)
        return response


class PresentationExceptionHandler:
    def __init__(self, logger: Logger):
        self.logger = logger

    @classmethod
    def create(cls) -> "PresentationExceptionHandler":
        return cls(logger=Logger("presentation_exception_handler"))

    def setup(self, app: fastapi.FastAPI):
        app.add_exception_handler(Error, self.error_handler)
        app.add_exception_handler(Exception, self.exception_handler)

    async def exception_handler(self, request: Request, exc: Exception):
        """
        実装上想定していない例外が発生した場合の処理
        :param Request request: リクエスト
        :param Exception exc: 例外
        :return PresentationJSONResponse: 500エラー
        """
        if request.state is not None and request.state.request_id is not None:
            self.logger.api_response_info(
                request_id=request.state.request_id,
                response_status_code=500,
            )
        self.logger.unexpected_error(exc)
        return PresentationJSONResponse(
            status=500,
            content={
                "message": "Internal Server Error",
            },
        )

    async def error_handler(self, request: Request, exc: Exception):
        """
        実装上想定したエラーだが、ユーザに表示する必要のないエラーが発生した場合の処理
        ユーザに表示する必要がないため、500エラーを返す
        :param Request request: リクエスト
        :param Exception exc: 例外
        :return PresentationJSONResponse: 500エラー
        """
        if request.state is not None and request.state.request_id is not None:
            self.logger.api_response_info(
                request_id=request.state.request_id,
                response_status_code=500,
            )
        self.logger.error(Error(exc))
        return PresentationJSONResponse(
            status=500,
            content={
                "message": "Internal Server Error",
            },
        )


T = TypeVar("T", bound=ApplicationBase)


def get_environment():
    return Environment()


class AppFactory(Generic[T]):
    def __init__(self, app_type: Type[T]):
        self.app_type = app_type

    def __call__(self, environment: Environment = Depends(get_environment)) -> T:
        return self.app_type.create(environment)


def get_application(app_type: Type[T]) -> T:
    return Depends(AppFactory(app_type))


PresentationTypeAuthorization = Annotated[str, Depends(
    OAuth2PasswordBearer(tokenUrl="token"))]


def get_admin_client_auth_application(
    environment: Environment = Depends(Environment)
) -> ApplicationAdminClientAuthOAuth2:
    return ApplicationAdminClientAuthOAuth2.create(environment)


def admin_client_authenticated(
    token: PresentationTypeAuthorization,
    application: ApplicationAdminClientAuthOAuth2 = Depends(
        get_admin_client_auth_application),
) -> DtoAdminClientId:
    try:
        result = application.oauth2(
            DtoAdminClientAuthToken(token=token))
    except ApplicationAdminClientAuthOAuth2Error as error:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


PresentationAdminClientAuthenticated = Annotated[DtoAdminClientId, Depends(
    admin_client_authenticated)]


class PresentationImageError(Exception):
    pass


class PresentationImage:
    async def __call__(self, image: UploadFile) -> Image.Image:
        content = await image.read()
        pil_image = Image.open(io.BytesIO(content))
        pil_image.load()
        if pil_image.format is None:
            raise PresentationImageError(
                f"image format is None: {image.filename}")
        return pil_image


PresentationTypeImage = Annotated[Image.Image, Depends(PresentationImage())]

PresentationTypeDatetime = Annotated[datetime, Form(...)]

PresentationTypeInt = Annotated[int, Form(...)]

PresentationTypeUUID = Annotated[uuid.UUID, Path(...)]
