from dataclasses import dataclass
from domain.person.flow_weight import DomainPersonFlowWeight
from typing import Iterator

@dataclass
class DomainPersonFlowWeightSequence:
    flow_weights: list[DomainPersonFlowWeight]

    def __iter__(self) -> Iterator[DomainPersonFlowWeight]:
        return iter(self.flow_weights)
