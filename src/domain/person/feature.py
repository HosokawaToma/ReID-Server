"""
人物の特徴量ドメインモデル

ReID 特徴量テンソルを保持し、同一人物判定の閾値比較を提供する。
"""
from dataclasses import dataclass, InitVar, field
import torch
from typing import ClassVar
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainPersonFeature(DomainUtilsBase):
    """
    人物の特徴量のドメインモデル。

    コサイン類似度が閾値以上なら同一人物とみなす。
    """
    feature: InitVar[torch.Tensor]
    _feature: torch.Tensor = field(init=False)
    THRESHOLD: ClassVar[float] = 0.895

    def __post_init__(self, feature: torch.Tensor) -> None:
        """
        不変性を保つために、torch.Tensor を複製して代入する。
        """
        object.__setattr__(self, "_feature", feature.detach().clone())

    def is_same(self, other: "DomainPersonFeature") -> bool:
        """
        他方の特徴量とのコサイン類似度が閾値以上かどうかを返す。

        :param DomainPersonFeature other: 比較する特徴量
        :return bool: 同一人物とみなす場合は True
        """
        if self._feature.device != other._feature.device:
            feature = other._feature.to(self._feature.device)
        else:
            feature = other._feature
        return torch.nn.functional.cosine_similarity(self._feature, feature, dim=0).item() > self.THRESHOLD
