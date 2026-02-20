"""
人物スナップショット DTO

検出結果のメタデータ・ゴミフラグ・人物ID・特徴量を保持する。
"""
import uuid
from dataclasses import dataclass
from datetime import datetime
import torch


@dataclass(frozen=True)
class DtoPersonSnapshot:
    """
    人物スナップショットを表す DTO。

    :param uuid.UUID id: スナップショットID
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: タイムスタンプ
    :param bool is_junk: ゴミデータかどうか
    :param uuid.UUID | None person_id: 人物ID（ゴミの場合は None）
    :param torch.Tensor | None feature: 特徴量（未抽出の場合は None）
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None
    feature: torch.Tensor | None
