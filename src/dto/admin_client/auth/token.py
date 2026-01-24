from dataclasses import dataclass

@dataclass(frozen=True)
class DtoAdminClientAuthToken:
    """
    アドミンクライアント認証トークンを表すDTO
    :param str token: トークン
    """
    token: str
