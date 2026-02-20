"""
アドミンクライアント認証資格情報 DTO

ログインID・パスワードを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoAdminClientAuthCredentials:
    """
    管理クライアント認証用の資格情報（ログインID・パスワード）を保持する DTO。
    """
    id: str
    password: str
