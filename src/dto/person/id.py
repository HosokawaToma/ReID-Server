"""
人物 ID DTO

人物の UUID とゴミフラグを保持する。
"""
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class DtoPersonId:
    """
    人物のIDを表すDTO
    :param uuid.UUID | None id: 人物のID（ゴミデータの場合はNone）
    :param bool is_junk: ゴミデータかどうか
    """
    id: uuid.UUID | None
    is_junk: bool
