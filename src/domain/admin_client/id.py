from dataclasses import dataclass

@dataclass
class DomainAdminClientId:
    """
    Admin Client IDを表すドメイン知識を集約する
    :param str id: ID
    """
    id: str
