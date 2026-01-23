from dataclasses import dataclass
import torch
from typing import ClassVar, Any
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainPersonFeature(DomainUtilsBase):
    """
    人物の特徴量のドメインモデル
    """
    feature: torch.Tensor
    THRESHOLD: ClassVar[float] = 0.895

    def __post_init__(self):
        cloned = self.feature.detach().clone()
        object.__setattr__(self, "feature", cloned)

    @property
    def value(self) -> torch.Tensor:
        return self.feature.clone()

    @property
    def shape(self):
        return self.feature.shape

    def is_same(self, other: "DomainPersonFeature") -> bool:
        return torch.nn.functional.cosine_similarity(self.feature, other.feature, dim=0).item() > self.THRESHOLD
