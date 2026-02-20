"""
HTTP ミドルウェア

リクエストID付与・APIログ・例外捕捉とエラーレスポンス返却を行う。
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from logger import Logger
from typing import Callable, Awaitable
import uuid
from error import (
    InternalServerError,
    BadGatewayError,
    ServiceUnavailableError,
    GatewayTimeoutError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    UnprocessableError,
    TooManyRequestsError,
    PayloadTooLargeError,
)
from presentation.utils.response import PresentationUtilJSONResponse


class PresentationUtilMiddleware(BaseHTTPMiddleware):
    """
    HTTPミドルウェア。リクエストIDの付与、APIログ、例外の捕捉とエラーレスポンス返却を行う。
    """

    def __init__(self, app: ASGIApp, logger: Logger):
        """
        ミドルウェアを初期化する。

        :param ASGIApp app: ASGIアプリケーション
        :param Logger logger: ロガー
        """
        super().__init__(app=app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """
        リクエストにIDを付与し、ログを出力したうえで次の処理を実行し、例外時はエラーレスポンスを返す。

        :param Request request: リクエスト
        :param Callable call_next: 次のミドルウェアまたはルートハンドラ
        :return Response: レスポンス
        """
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        self.logger.api_request_info(
            request_id=request_id, request_path=request.url.path, request_method=request.method)
        try:
            response = await call_next(request)
        except InternalServerError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=500, content={
                "message": "Internal Server Error",
            })
        except BadGatewayError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=502, content={
                "message": "Bad Gateway",
            })
        except ServiceUnavailableError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=503, content={
                "message": "Service Unavailable",
            })
        except GatewayTimeoutError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=504, content={
                "message": "Gateway Timeout",
            })
        except AuthenticationError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=401, content={
                "message": "Unauthorized",
            })
        except AuthorizationError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=403, content={
                "message": "Forbidden",
            })
        except ValidationError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=400, content={
                "message": "Bad Request",
            })
        except NotFoundError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=404, content={
                "message": "Not Found",
            })
        except UnprocessableError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=422, content={
                "message": "Unprocessable Entity",
            })
        except TooManyRequestsError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=429, content={
                "message": "Too Many Requests",
            })
        except PayloadTooLargeError as e:
            self.logger.error(error=e, id=request_id)
            return PresentationUtilJSONResponse(status=413, content={
                "message": "Payload Too Large",
            })
        except Exception as e:
            self.logger.unexpected_error(exception=e, id=request_id)
            return PresentationUtilJSONResponse(status=500, content={
                "message": "Internal Server Error",
            })
        self.logger.api_response_info(
            request_id=request_id, response_status_code=response.status_code)
        return response
