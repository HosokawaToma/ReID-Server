from dataclasses import dataclass
from domain.camera_frame import DomainCameraFrame

@dataclass
class DomainCameraFrameSequence:
    frames: list[DomainCameraFrame]
