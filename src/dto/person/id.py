"""
人物 ID DTO

人物の UUID とゴミフラグを保持する。
"""
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class DtoPersonId:
    """
    人物ID を保持する DTO。人物の UUID とゴミフラグを API で渡す際に用いる。ゴミの場合は id が None。
    """
    id: uuid.UUID | None
    is_junk: bool
