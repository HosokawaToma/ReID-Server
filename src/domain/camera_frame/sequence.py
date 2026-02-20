"""
カメラフレームシーケンスのドメインモデル

カメラフレームのリストを保持する。
"""
from dataclasses import dataclass
from domain.camera_frame import DomainCameraFrame
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainCameraFrameSequence(DomainUtilsSequenceBase[DomainCameraFrame]):
    """カメラフレームのシーケンス。"""
    pass
