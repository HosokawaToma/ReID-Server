"""
人物の特徴量ドメインモデル

ReID（人物再同定）モデルが出力する特徴量ベクトルを保持し、同一人物かどうかの判定を提供する。
特徴量は不変として扱い、受け取り時に複製して保持する。
同一人物判定はコサイン類似度が 0.895 以上であることをもって行う。
"""
from dataclasses import dataclass, InitVar, field
import torch
from typing import ClassVar
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainPersonFeature(DomainUtilsBase):
    """
    人物の特徴量のドメインモデル。

    ReID モデルが抽出した 1 次元の特徴ベクトルを保持する。
    二つの特徴量が同一人物かどうかは、コサイン類似度が 0.895 以上かどうかで判定する。
    比較対象が別デバイス上にある場合は、同一デバイスに揃えてから比較する。
    """
    feature: InitVar[torch.Tensor]
    _feature: torch.Tensor = field(init=False)
    THRESHOLD: ClassVar[float] = 0.895

    def __post_init__(self, feature: torch.Tensor) -> None:
        """
        受け取った特徴ベクトルを複製して保持する。元のテンソルの変更は反映されない。
        """
        object.__setattr__(self, "_feature", feature.detach().clone())

    def is_same(self, other: "DomainPersonFeature") -> bool:
        """
        もう一方の特徴量とのコサイン類似度が 0.895 以上なら同一人物とみなす。

        比較対象が別デバイス上にある場合は、このインスタンスのデバイスに転送してから比較する。

        :param DomainPersonFeature other: 比較するもう一方の特徴量
        :return bool: 同一人物とみなす場合 True、そうでなければ False
        """
        if self._feature.device != other._feature.device:
            feature = other._feature.to(self._feature.device)
        else:
            feature = other._feature
        return torch.nn.functional.cosine_similarity(self._feature, feature, dim=0).item() > self.THRESHOLD
