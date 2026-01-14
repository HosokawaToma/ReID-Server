from dataclasses import dataclass, field
import uuid
from value.utils import ValueUtilsBase

@dataclass
class ValueId(ValueUtilsBase):
    """
    値オブジェクトとしてのID
    :param uuid.UUID id: ID
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)
