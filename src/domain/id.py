from dataclasses import dataclass
import uuid

@dataclass
class DomainId:
    """
    IDを表すドメイン知識を集約する
    :param uuid.UUID id: ID
    """
    id: uuid.UUID
