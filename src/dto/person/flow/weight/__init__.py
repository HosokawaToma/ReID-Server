from dataclasses import dataclass

@dataclass
class DtoPersonFlowWeight:
    target_camera_id: int
    source_camera_id: int
    weight: int
