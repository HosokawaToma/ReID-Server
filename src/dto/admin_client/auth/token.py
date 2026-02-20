"""
アドミンクライアント認証トークン DTO

JWT 文字列を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoAdminClientAuthToken:
    """
    管理クライアント認証用のアクセストークン（JWT 文字列）を保持する DTO。
    """
    token: str
