from dataclasses import dataclass

@dataclass
class EntityPersonFlowWeight:
    target_camera_id: int
    source_camera_id: int
    weight: int
