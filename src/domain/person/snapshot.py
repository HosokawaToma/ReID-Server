import uuid
from dataclasses import dataclass, field
from typing import ClassVar
import torch
from datetime import datetime
from PIL import Image
from domain.yolo.pose_model import DomainYoloPoseModel
from domain.yolo.segment_model import DomainYoloSegmentModel
from modules.reid.model import ModuleReIDModel
from error import Error


class DomainPersonSnapshotError(Error):
    pass


class DomainPersonSnapshotSelfJunkError(DomainPersonSnapshotError):
    pass


class DomainPersonSnapshotOtherJunkError(DomainPersonSnapshotError):
    pass


class DomainPersonSnapshotDateNotSameError(DomainPersonSnapshotError):
    pass


class DomainPersonSnapshotPersonOtherIdNotSetError(DomainPersonSnapshotError):
    pass


class DomainPersonSnapshotFeatureNotSetError(DomainPersonSnapshotError):
    pass


@dataclass
class DomainPersonSnapshot:
    MATCH_THRESHOLD: ClassVar[float] = 0.895
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime
    _is_junk: bool = True
    feature: torch.Tensor | None = None
    person_id: uuid.UUID | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @property
    def is_junk(self) -> bool:
        return self._is_junk

    @is_junk.setter
    def is_junk(self, value: bool) -> None:
        if value == True:
            self.feature = None
            self.person_id = None
        self._is_junk = value

    def detect_junk(self, pose_model: DomainYoloPoseModel, segment_model: DomainYoloSegmentModel) -> None:
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

    def extract_feature(self, reid_model: ModuleReIDModel) -> None:
        """
        画像から特徴量を抽出する
        ジャンクのPersonSnapshotは、採用対象外のためエラーを発生させる
        :param ModuleReIDModel reid_model: 特徴量抽出モデル
        """
        if self.is_junk:
            raise DomainPersonSnapshotSelfJunkError()
        self.feature = reid_model.extract_feature(self.image, self.camera_id, self.view_id)

    def person_reid(self, other: "DomainPersonSnapshot | None" = None) -> None:
        """
        特徴量が閾値以上の場合、同一人物と見做し、同じperson_idを設定する
        比較対象が未設定の場合、新しい人物と見做し、新しいperson_idを設定する
        ジャンクのPersonSnapshotは、採用対象外のためエラーを発生させる
        日付が異なるPersonSnapshotは、必ず異なる人物と見做すためエラーを発生させる
        人物IDが未設定のPersonSnapshotは、採用対象外のためエラーを発生させる
        特徴量が未設定のPersonSnapshotは、採用対象外のためエラーを発生させる
        :param DomainPersonSnapshot | None other: 比較対象のPersonSnapshot
        """
        if self.is_junk:
            raise DomainPersonSnapshotSelfJunkError()
        self.person_id = uuid.uuid4()
        if other is None:
            return
        if other.is_junk:
            raise DomainPersonSnapshotOtherJunkError()
        if datetime.combine(self.timestamp.date(), datetime.min.time()) != datetime.combine(other.timestamp.date(), datetime.min.time()):
            raise DomainPersonSnapshotDateNotSameError()
        if other.person_id is None:
            raise DomainPersonSnapshotPersonOtherIdNotSetError()
        if self.feature is None or other.feature is None:
            raise DomainPersonSnapshotFeatureNotSetError()
        if torch.nn.functional.cosine_similarity(self.feature, other.feature, dim=0).item() > self.MATCH_THRESHOLD:
            self.person_id = other.person_id
