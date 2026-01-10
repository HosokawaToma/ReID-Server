from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class DtoPersonFlowWeightQuery:
    """
    人物フロー重みクエリを表すDTO
    :param datetime timestamp_after: タイムスタンプ以降
    :param datetime timestamp_before: タイムスタンプ以前
    :param list[uuid.UUID] person_ids: 人物IDリスト
    """
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    person_ids: list[uuid.UUID] | None = None
