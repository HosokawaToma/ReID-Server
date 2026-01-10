from dataclasses import dataclass
import uuid
import torch
from datetime import datetime
from typing import ClassVar

from error import Error

class DomainPersonSnapshotFeatureError(Error):
    pass

class DomainPersonSnapshotFeatureSelfJunkError(DomainPersonSnapshotFeatureError):
    pass

class DomainPersonSnapshotFeatureOtherJunkError(DomainPersonSnapshotFeatureError):
    pass

class DomainPersonSnapshotFeatureDateNotSameError(DomainPersonSnapshotFeatureError):
    pass

class DomainPersonSnapshotFeaturePersonOtherIdNotSetError(DomainPersonSnapshotFeatureError):
    pass

class DomainPersonSnapshotFeatureFeatureNotSetError(DomainPersonSnapshotFeatureError):
    pass

@dataclass
class DomainPersonSnapshotFeature:
    """
    人物検出の特徴量に関するドメイン知識を集約する
    :param uuid.UUID id: 人物検出のID
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: タイムスタンプ
    :param bool is_junk: ジャンクフラグ
    :param torch.Tensor feature: 特徴量
    :param uuid.UUID | None person_id: 人物ID
    """
    MATCH_THRESHOLD: ClassVar[float] = 0.895
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    feature: torch.Tensor
    person_id: uuid.UUID | None = None

    def person_reid(self, other: "DomainPersonSnapshotFeature | None" = None) -> None:
        """
        特徴量が閾値以上の場合、同一人物と見做し、同じperson_idを設定する
        比較対象が未設定の場合、新しい人物と見做し、新しいperson_idを設定する
        ジャンクのPersonSnapshotは、採用対象外のためエラーを発生させる
        日付が異なるPersonSnapshotは、必ず異なる人物と見做すためエラーを発生させる
        人物IDが未設定のPersonSnapshotは、採用対象外のためエラーを発生させる
        特徴量が未設定のPersonSnapshotは、採用対象外のためエラーを発生させる
        :param DomainPersonSnapshotFeature | None other: 比較対象のPersonSnapshotFeature
        """
        if self.is_junk:
            raise DomainPersonSnapshotFeatureSelfJunkError()
        self.person_id = uuid.uuid4()
        if other is None:
            return
        if other.is_junk:
            raise DomainPersonSnapshotFeatureOtherJunkError()
        if datetime.combine(self.timestamp.date(), datetime.min.time()) != datetime.combine(other.timestamp.date(), datetime.min.time()):
            raise DomainPersonSnapshotFeatureDateNotSameError()
        if other.person_id is None:
            raise DomainPersonSnapshotFeaturePersonOtherIdNotSetError()
        if self.feature is None or other.feature is None:
            raise DomainPersonSnapshotFeatureFeatureNotSetError()
        if torch.nn.functional.cosine_similarity(self.feature, other.feature, dim=0).item() > self.MATCH_THRESHOLD:
            self.person_id = other.person_id
