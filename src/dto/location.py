from dataclasses import dataclass

@dataclass(frozen=True)
class DtoLocation:
    camera_id: int
    view_id: int
