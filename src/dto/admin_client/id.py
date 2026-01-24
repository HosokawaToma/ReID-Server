from dataclasses import dataclass

@dataclass(frozen=True)
class DtoAdminClientId:
    """
    Admin Client IDを表すDTO
    :param str id: ID
    """
    id: str
