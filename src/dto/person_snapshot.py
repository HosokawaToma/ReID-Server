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
    人物検出結果（スナップショット）を保持する DTO。

    識別子・カメラID・ビューID・タイムスタンプ・ゴミフラグ・人物ID・特徴量（未抽出時は None）を API で受け渡す際に用いる。
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None
    feature: torch.Tensor | None
