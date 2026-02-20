"""
人物フロー重み DTO

地点間の移動人数（重み）を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoPersonFlowWeight:
    """
    人物フロー重みを保持する DTO。

    地点間の移動人数を、ターゲットカメラID・ソースカメラID・重み（人数）で表す。
    """
    target_camera_id: int
    source_camera_id: int
    weight: int
