from dataclasses import dataclass

@dataclass(frozen=True)
class DtoPersonFlowWeight:
    """
    人物フロー重みを表すDTO
    :param int target_camera_id: ターゲットカメラID
    :param int source_camera_id: ソースカメラID
    :param int weight: 重み
    """
    target_camera_id: int
    source_camera_id: int
    weight: int
