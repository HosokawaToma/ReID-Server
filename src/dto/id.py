from dataclasses import dataclass
import uuid

@dataclass
class DtoId:
    """
    IDを表すDTO
    :param uuid.UUID id: ID
    """
    id: uuid.UUID
