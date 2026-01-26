from dataclasses import dataclass, InitVar, field
import torch
from typing import ClassVar
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainPersonFeature(DomainUtilsBase):
    """
    人物の特徴量のドメインモデル
    """
    feature: InitVar[torch.Tensor]
    _feature: torch.Tensor = field(init=False)
    THRESHOLD: ClassVar[float] = 0.895

    def __post_init__(self, feature: torch.Tensor):
        """
        不変性を保つために、torch.Tensorを複製して代入する
        """
        object.__setattr__(self, "_feature", feature.detach().clone())

    def is_same(self, other: "DomainPersonFeature") -> bool:
        if self._feature.device != other._feature.device:
            feature = other._feature.to(self._feature.device)
        else:
            feature = other._feature
        return torch.nn.functional.cosine_similarity(self._feature, feature, dim=0).item() > self.THRESHOLD
