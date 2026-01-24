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

    @property
    def value(self) -> torch.Tensor:
        return self._feature.clone()

    @property
    def shape(self):
        return self._feature.shape

    def is_same(self, other: "DomainPersonFeature") -> bool:
        return torch.nn.functional.cosine_similarity(self._feature, other._feature, dim=0).item() > self.THRESHOLD
