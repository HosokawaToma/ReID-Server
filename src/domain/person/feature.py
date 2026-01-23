from dataclasses import dataclass
import torch
from typing import ClassVar
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainPersonFeature(DomainUtilsBase):
    """
    人物の特徴量のドメインモデル
    """
    feature: torch.Tensor
    THRESHOLD: ClassVar[float] = 0.895

    def is_same(self, other: "DomainPersonFeature") -> bool:
        return torch.nn.functional.cosine_similarity(self.feature, other.feature, dim=0).item() > self.THRESHOLD
