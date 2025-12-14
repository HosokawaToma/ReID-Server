import uuid
from dataclasses import dataclass, field
from typing import ClassVar
import torch
from datetime import datetime
from PIL import Image
from domain.yolo.pose_model import DomainYoloPoseModel
from domain.yolo.segment_model import DomainYoloSegmentModel
from modules.reid.model import ModuleReIDModel

@dataclass
class DomainPersonSnapshot:
    MATCH_THRESHOLD: ClassVar[float] = 0.895
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime
    feature: torch.Tensor | None = None
    person_id: uuid.UUID | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def is_full_body(self, pose_model: DomainYoloPoseModel) -> bool:
        key_points = pose_model.extract(self.image)
        if len(key_points) != 1:
            return False
        if not key_points[0].is_confidence():
            return False
        return True

    def is_one_person(self, segment_model: DomainYoloSegmentModel) -> bool:
        masks = segment_model.extract(self.image)
        if len(masks) != 1:
            return False
        return True

    def extract_feature(self, reid_model: ModuleReIDModel) -> None:
        self.feature = reid_model.extract_feature(self.image, self.camera_id, self.view_id)

    def has_feature(self) -> bool:
        return self.feature is not None

    def person_reid(self, other: "DomainPersonSnapshot") -> None:
        if self.feature is None or other.feature is None:
            return
        if torch.nn.functional.cosine_similarity(self.feature, other.feature, dim=0).item() > self.MATCH_THRESHOLD:
            self.person_id = other.person_id
