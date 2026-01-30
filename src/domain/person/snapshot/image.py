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
from domain.person.feature import DomainPersonFeature

@dataclass(frozen=True)
class DomainPersonSnapshotImage(DomainUtilsBase):
    """
    人物検出結果の画像のドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    image: DomainImage
    feature: DomainPersonFeature
    person_id: DomainPersonId

    def detect_junk(
        self,
        instance_segmenter: DomainYoloInstanceSegmenter,
        pose_estimator: DomainYoloPoseEstimator,
    ) -> "DomainPersonSnapshotImage":
        """
        人物検出結果の画像からゴミデータを判定する
        画像に全身が写っておらず、かつ一人のみ写った画像以外はゴミデータと判定する
        :param DomainYoloInstanceSegmenter instance_segmenter: 個体推定器
        :param DomainYoloPoseEstimator pose_estimator: 姿勢推定器
        :return DomainPersonSnapshotImage: ゴミデータを判定した人物検出結果の画像
        """
        instances = instance_segmenter.extract(self.image)
        if not instances.is_one_person():
            return DomainPersonSnapshotImage(
                id=self.id,
                location=self.location,
                timestamp=self.timestamp,
                image=self.image,
                feature=self.feature,
                person_id=DomainPersonId.junk(),
            )
        poses = pose_estimator.extract(self.image)
        if not poses.is_one_person():
            return DomainPersonSnapshotImage(
                id=self.id,
                location=self.location,
                timestamp=self.timestamp,
                image=self.image,
                feature=self.feature,
                person_id=DomainPersonId.junk(),
            )
        pose = poses.one_person()
        if not pose.is_full_length():
            return DomainPersonSnapshotImage(
                id=self.id,
                location=self.location,
                timestamp=self.timestamp,
                image=self.image,
                feature=self.feature,
                person_id=DomainPersonId.junk(),
            )
        return DomainPersonSnapshotImage(
            id=self.id,
            location=self.location,
            timestamp=self.timestamp,
            image=self.image,
            feature=self.feature,
            person_id=DomainPersonId.new_id(),
        )

    def extract_feature(self, reid_model: DomainReIDModel) -> DomainPersonSnapshotFeature:
        """
        人物検出結果の画像から特徴量を抽出する
        :param DomainReIDModel reid_model: ReIDモデル
        :return DomainPersonSnapshotFeature: 特徴量を抽出した人物検出結果の特徴量
        """
        return DomainPersonSnapshotFeature(
            id=self.id,
            location=self.location,
            timestamp=self.timestamp,
            feature=reid_model.extract(image=self.image, location=self.location),
            person_id=DomainPersonId.new_id(),
        )
