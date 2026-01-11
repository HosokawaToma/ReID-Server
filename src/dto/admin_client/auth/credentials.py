from dataclasses import dataclass

@dataclass
class DtoAdminClientAuthCredentials:
    """
    アドミンクライアント認証資格情報を表すDTO
    :param str id: ログインID
    :param str password: パスワード
    """
    id: str
    password: str
