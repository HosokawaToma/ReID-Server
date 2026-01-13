from dataclasses import dataclass, field
import uuid

@dataclass
class DomainIdValue:
    """
    IDを表す値オブジェクト
    :param uuid.UUID id: ID
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)
