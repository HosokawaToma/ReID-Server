from dataclasses import dataclass, field
import uuid
from PIL import Image
from datetime import datetime

from domain.yolo.pose_model import DomainYoloPoseModel
from domain.yolo.segment_model import DomainYoloSegmentModel
from error import Error
from modules.reid.model import ModuleReIDModel
from domain.person.snapshot.feature import DomainPersonSnapshotFeature

class DomainPersonSnapshotImageError(Error):
    pass

class DomainPersonSnapshotImageSelfJunkError(DomainPersonSnapshotImageError):
    pass

@dataclass
class DomainPersonSnapshotImage:
    """
    人物検出の画像に関するドメイン知識を集約する
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: タイムスタンプ
    :param Image.Image image: 画像
    :param bool | None is_junk: ジャンクフラグ
    :param uuid.UUID id: 人物検出のID
    """
    camera_id: int
    view_id: int
    timestamp: datetime
    image: Image.Image
    is_junk: bool = field(default=True)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def detect_junk(
        self,
        pose_model: DomainYoloPoseModel,
        segment_model: DomainYoloSegmentModel,
    ) -> None:
        """
        不採用なPersonSnapshotかどうかを検出する
        :param DomainYoloPoseModel pose_model: 姿勢推定モデル
        :param DomainYoloSegmentModel segment_model: 個別物体推定モデル
        """
        if not pose_model.is_full_body(self.image):
            self.is_junk = True
            return
        if not segment_model.is_one_person(self.image):
            self.is_junk = True
            return
        self.is_junk = False

    def extract_feature(self, reid_model: ModuleReIDModel) -> DomainPersonSnapshotFeature:
        """
        画像から特徴量を抽出する
        :param ModuleReIDModel reid_model: 特徴量抽出モデル
        """
        if self.is_junk:
            raise DomainPersonSnapshotImageSelfJunkError()
        feature = reid_model.extract_feature(self.image, self.camera_id, self.view_id)
        return DomainPersonSnapshotFeature(
            id=self.id,
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
            is_junk=self.is_junk,
            feature=feature,
        )
