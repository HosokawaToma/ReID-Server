"""
汎用 ID DTO

UUID を保持する。
"""
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class DtoId:
    """
    汎用の識別子を保持する DTO。

    UUID を 1 つ保持する。各種リソースの ID として API で受け渡す。

    :param uuid.UUID id: 識別子
    """
    id: uuid.UUID
