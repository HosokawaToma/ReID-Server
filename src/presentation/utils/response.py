"""
プレゼンテーション用レスポンス

JSONレスポンスと画像ストリーミングレスポンスを提供する。
"""
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from dto.image import DtoImage
import io
from typing import Any
from datetime import timedelta


class PresentationUtilJSONResponse(JSONResponse):
    """
    JSON レスポンスに加え、Cookie へリフレッシュトークンを設定する機能を提供する。
    """
    REFRESH_TOKEN_MAX_AGE = int(timedelta(days=1).total_seconds())

    def __init__(self, status: int, content: dict[str, Any]):
        """
        JSONレスポンスを初期化する。

        :param int status: HTTPステータスコード
        :param dict[str, Any] content: JSONの内容
        """
        super().__init__(content=content, status_code=status)

    def set_refresh_token(self, refresh_token: str) -> None:
        """
        Cookie にリフレッシュトークンを設定する。

        :param str refresh_token: リフレッシュトークン
        """
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
    """
    画像をストリーミングで返すレスポンス。

    画像のバイト列とフォーマットから Content-Type（image/xxx）を設定する。
    """

    def __init__(self, status: int, image: DtoImage):
        """
        画像レスポンスを初期化する。

        :param int status: HTTPステータスコード
        :param DtoImage image: 画像DTO
        """
        super().__init__(
            content=io.BytesIO(image.bytes),
            media_type=f"image/{image.format.lower()}",
            status_code=status,
        )
