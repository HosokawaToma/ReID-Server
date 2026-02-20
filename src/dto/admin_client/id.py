"""
アドミンクライアント ID DTO

クライアント識別子を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoAdminClientId:
    """
    管理クライアントの識別子を保持する DTO。認証済みクライアントを表す際に用いる。
    """
    id: str
