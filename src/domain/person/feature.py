from dataclasses import dataclass
import torch
from typing import ClassVar
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainPersonFeature(DomainUtilsBase):
    """
    人物の特徴量のドメインモデル
    """
    list: list[float]
    THRESHOLD: ClassVar[float] = 0.895

    @classmethod
    def from_tensor(cls, tensor: torch.Tensor) -> "DomainPersonFeature":
        return cls(list=tensor.cpu().numpy().tolist())

    @property
    def tensor(self) -> torch.Tensor:
        return torch.tensor(self.list)

    def is_same(self, other: "DomainPersonFeature") -> bool:
        return torch.nn.functional.cosine_similarity(self.tensor, other.tensor, dim=0).item() > self.THRESHOLD
