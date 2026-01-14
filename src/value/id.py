from dataclasses import dataclass, field
import uuid

@dataclass
class ValueId:
    """
    値オブジェクトとしてのID
    :param uuid.UUID id: ID
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)
