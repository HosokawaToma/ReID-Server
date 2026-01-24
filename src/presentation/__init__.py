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
import io
from datetime import datetime
from fastapi import Request, Response
from applications.admin_client.auth.oauth2 import ApplicationAdminClientAuthOAuth2
from error import (
    InternalServerError,
    BadGatewayError,
    ServiceUnavailableError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    UnprocessableError,
    TooManyRequestsError,
    PayloadTooLargeError,
)
from dto.admin_client.auth.token import DtoAdminClientAuthToken
from dto.admin_client.id import DtoAdminClientId
from environment import Environment
from pydantic import BaseModel
import uuid
from logger import Logger
from applications import ApplicationBase
from dto.image import DtoImage
import pathlib


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


class PresentationImageResponse(StreamingResponse):
    def __init__(self, status: int, image: DtoImage):
        super().__init__(
            content=io.BytesIO(image.bytes),
            media_type=f"image/{image.format.lower()}",
            status_code=status,
        )


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
        try:
            response = await call_next(request)
        except InternalServerError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=500, content={
                "message": "Internal Server Error",
            })
        except BadGatewayError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=502, content={
                "message": "Bad Gateway",
            })
        except ServiceUnavailableError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=503, content={
                "message": "Service Unavailable",
            })
        except AuthenticationError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=401, content={
                "message": "Unauthorized",
            })
        except AuthorizationError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=403, content={
                "message": "Forbidden",
            })
        except ValidationError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=400, content={
                "message": "Bad Request",
            })
        except NotFoundError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=404, content={
                "message": "Not Found",
            })
        except UnprocessableError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=422, content={
                "message": "Unprocessable Entity",
            })
        except TooManyRequestsError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=429, content={
                "message": "Too Many Requests",
            })
        except PayloadTooLargeError as e:
            self.logger.error(e)
            return PresentationJSONResponse(status=413, content={
                "message": "Payload Too Large",
            })
        except Exception as e:
            self.logger.unexpected_error(e)
            return PresentationJSONResponse(status=500, content={
                "message": "Internal Server Error",
            })
        self.logger.api_response_info(request_id=request_id, response_status_code=response.status_code)
        return response


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
    except AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


PresentationAdminClientAuthenticated = Annotated[DtoAdminClientId, Depends(
    admin_client_authenticated)]


class PresentationImage:
    async def __call__(self, image: UploadFile) -> DtoImage:
        if image.filename is None:
            raise NotFoundError("image filename is None")
        content = await image.read()
        format = pathlib.Path(image.filename).suffix[1:]
        if format == "":
            raise NotFoundError("image format is empty")
        return DtoImage(bytes=content, format=format.lower())


PresentationTypeImage = Annotated[DtoImage, Depends(PresentationImage())]

PresentationTypeDatetime = Annotated[datetime, Form(...)]

PresentationTypeInt = Annotated[int, Form(...)]

PresentationTypeUUID = Annotated[uuid.UUID, Path(...)]
