"""
アドミンクライアント認証結果 DTO

アクセストークン・リフレッシュトークンを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoAdminClientAuthResult:
    """
    アドミンクライアント認証結果を表すDTO
    :param str token: トークン
    :param str refresh_token: リフレッシュトークン
    """
    token: str
    refresh_token: str
