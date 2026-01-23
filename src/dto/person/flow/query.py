from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass(frozen=True)
class DtoPersonFlowQuery:
    """
    人物フロークエリを表すDTO
    :param uuid.UUID person_id: 人物ID
    :param datetime timestamp_after: タイムスタンプ以降
    :param datetime timestamp_before: タイムスタンプ以前
    """
    person_id: uuid.UUID
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
