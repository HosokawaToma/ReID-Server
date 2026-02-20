"""
ReID モデルのドメインラッパー

画像・位置から人物特徴量を抽出する。
"""
from dataclasses import dataclass
from domain.image import DomainImage
from domain.location import DomainLocation
from domain.person.feature import DomainPersonFeature
from domain.utils.base import DomainUtilsBase
from modules.reid.model import ModuleReIDModel


@dataclass(frozen=True)
class DomainReIDModel(DomainUtilsBase):
    """
    ReID モデルのドメインラッパー。

    モジュールの ReID モデルを保持し、extract で特徴量を返す。
    """
    model: ModuleReIDModel

    def extract(self, image: DomainImage, location: DomainLocation) -> DomainPersonFeature:
        """
        画像と位置から人物特徴量を抽出する。

        :param DomainImage image: 入力画像
        :param DomainLocation location: 撮影位置
        :return DomainPersonFeature: 特徴量
        """
        return DomainPersonFeature(
            feature=self.model.extract_feature(
                image=image.image,
                camera_id=location.camera_id,
                view_id=location.view_id
            ),
        )
