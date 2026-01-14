from dataclasses import dataclass, field
import uuid

@dataclass
class DomainIdValue:
    """
    非推奨
    代わりに ValueId を使用する
    IDを表す値オブジェクト
    :param uuid.UUID id: ID
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)
