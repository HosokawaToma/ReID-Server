from dataclasses import dataclass
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.image import DomainImage
from domain.person.id import DomainPersonId
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from domain.utils.base import DomainUtilsBase
from domain.reid.model import DomainReIDModel
from domain.person.snapshot.feature import DomainPersonSnapshotFeature


@dataclass(frozen=True)
class DomainPersonSnapshotImage(DomainUtilsBase):
    """
    人物検出結果の画像のドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    image: DomainImage
    person_id: DomainPersonId

    def detect_junk(
        self,
        instance_segmenter: DomainYoloInstanceSegmenter,
        pose_estimator: DomainYoloPoseEstimator,
    ) -> "DomainPersonSnapshotImage":
        instances = instance_segmenter.extract(self.image)
        if not instances.is_one_person():
            return DomainPersonSnapshotImage(
                id=self.id,
                location=self.location,
                timestamp=self.timestamp,
                image=self.image,
                person_id=self.person_id.junk(),
            )
        poses = pose_estimator.extract(self.image)
        if not poses.is_one_person():
            return DomainPersonSnapshotImage(
                id=self.id,
                location=self.location,
                timestamp=self.timestamp,
                image=self.image,
                person_id=self.person_id.junk(),
            )
        pose = poses.one_person()
        if not pose.is_full_length():
            return DomainPersonSnapshotImage(
                id=self.id,
                location=self.location,
                timestamp=self.timestamp,
                image=self.image,
                person_id=self.person_id.junk(),
            )
        return DomainPersonSnapshotImage(
            id=self.id,
            location=self.location,
            timestamp=self.timestamp,
            image=self.image,
            person_id=self.person_id.new_id(),
        )

    def extract_feature(self, reid_model: DomainReIDModel) -> DomainPersonSnapshotFeature:
        return DomainPersonSnapshotFeature(
            id=self.id,
            location=self.location,
            timestamp=self.timestamp,
            feature=reid_model.extract(image=self.image, location=self.location),
            person_id=self.person_id,
        )
