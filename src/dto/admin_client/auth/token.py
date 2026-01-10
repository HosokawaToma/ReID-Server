from dataclasses import dataclass

@dataclass
class DtoAdminClientAuthToken:
    """
    アドミンクライアント認証トークンを表すDTO
    :param str token: トークン
    """
    token: str
