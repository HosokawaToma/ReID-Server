"""
アドミンクライアント認証資格情報 DTO

ログインID・パスワードを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoAdminClientAuthCredentials:
    """
    アドミンクライアント認証資格情報を表すDTO
    :param str id: ログインID
    :param str password: パスワード
    """
    id: str
    password: str
