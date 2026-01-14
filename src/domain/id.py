from dataclasses import dataclass
import uuid

@dataclass
class DomainId:
    """
    非推奨
    代わりに ValueId を使用する
    IDを表すドメイン知識を集約する
    :param uuid.UUID id: ID
    """
    id: uuid.UUID
