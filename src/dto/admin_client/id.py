from dataclasses import dataclass

@dataclass
class DtoAdminClientId:
    """
    Admin Client IDを表すDTO
    :param str id: ID
    """
    id: str
