from dataclasses import dataclass

@dataclass
class EntityPersonFlowWeight:
    source_camera_id: int
    target_camera_id: int
    weight: float

    def to_dict(self) -> dict:
        return {
            "source_camera_id": self.source_camera_id,
            "target_camera_id": self.target_camera_id,
            "weight": self.weight,
        }
