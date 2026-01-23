from dataclasses import dataclass
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.image import DomainImage
from domain.yolo.object_detector import DomainYoloObjectDetector
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from domain.person.snapshot.image_sequence import DomainPersonSnapshotImageSequence
from domain.person.snapshot.image import DomainPersonSnapshotImage
from domain.person.id import DomainPersonId
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainCameraFrameImage(DomainUtilsBase):
    """
    カメラフレーム画像のドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    image: DomainImage

    def create_person_snapshot_images(
        self,
        yolo_object_detector: DomainYoloObjectDetector,
        yolo_instance_segmenter: DomainYoloInstanceSegmenter,
        yolo_pose_estimator: DomainYoloPoseEstimator,
        ) -> DomainPersonSnapshotImageSequence:
        """
        カメラフレーム画像から人物検出結果の画像を生成する
        同時に人物検出画像のゴミデータ判定を行う
        :param DomainYoloObjectDetector yolo_object_detector: 物体検出器
        :param DomainYoloInstanceSegmenter yolo_instance_segmenter: 個体推定器
        :param DomainYoloPoseEstimator yolo_pose_estimator: 姿勢推定器
        :return DomainPersonSnapshotImageSequence: 人物検出結果の画像のシーケンス
        """
        bounding_boxes = yolo_object_detector.extract_person(image=self.image)
        return DomainPersonSnapshotImageSequence(items=[
            DomainPersonSnapshotImage(
                id=DomainId(),
                location=self.location,
                timestamp=self.timestamp,
                image=self.image.crop(
                    x1=bounding_box.x1,
                    y1=bounding_box.y1,
                    x2=bounding_box.x2,
                    y2=bounding_box.y2,
                ),
                person_id=DomainPersonId(),
            ) for bounding_box in bounding_boxes
        ]).detect_junk(yolo_instance_segmenter, yolo_pose_estimator)
