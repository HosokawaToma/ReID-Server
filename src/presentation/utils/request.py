"""
プレゼンテーション用リクエスト

リクエストID・リフレッシュトークン取得の拡張を提供する。
"""
from fastapi import Request
from pydantic import BaseModel


class PresentationUtilRequest(Request):
    """
    FastAPI の Request を拡張し、リクエストIDとリフレッシュトークンの取得を提供する。
    """
    UNKNOWN_REQUEST_ID = "unknown"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_refresh_token(self) -> str:
        """
        Cookie からリフレッシュトークンを取得する。

        :return str: リフレッシュトークン（無い場合は空文字）
        """
        return self.cookies.get("refresh_token", "")

    def get_request_id(self) -> str:
        """
        ミドルウェアで付与されたリクエストIDを取得する。未設定の場合は "unknown" を返す。

        :return str: リクエストID
        """
        if self.state is not None:
            return getattr(self.state, "request_id", self.UNKNOWN_REQUEST_ID)
        else:
            return self.UNKNOWN_REQUEST_ID


class PresentationUtilRequestBody(BaseModel):
    """
    プレゼンテーション層のリクエストボディの基底。Pydantic の BaseModel を継承する。
    """
    pass
