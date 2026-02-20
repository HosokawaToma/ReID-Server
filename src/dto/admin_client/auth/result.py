"""
アドミンクライアント認証結果 DTO

アクセストークン・リフレッシュトークンを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoAdminClientAuthResult:
    """
    管理クライアント認証結果を保持する DTO。アクセストークンとリフレッシュトークンを API のレスポンスで返す際に用いる。
    """
    token: str
    refresh_token: str
