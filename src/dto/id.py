"""
汎用 ID DTO

UUID を保持する。
"""
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class DtoId:
    """
    IDを表すDTO
    :param uuid.UUID id: ID
    """
    id: uuid.UUID
