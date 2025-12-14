from dataclasses import dataclass
from domain.person.flow import DomainPersonFlow
from domain.person.flow_weight import DomainPersonFlowWeight
from domain.person.flow_weight_sequence import DomainPersonFlowWeightSequence
from typing import Iterator

@dataclass
class DomainPersonFlowSequence:
    flows: list[DomainPersonFlow]

    def __iter__(self) -> Iterator[DomainPersonFlow]:
        return iter(self.flows)

    def to_weights(self) -> DomainPersonFlowWeightSequence:
        weights: dict[tuple[int, int], int] = {}
        for item in self.flows:
            key = (item.source_camera_id, item.target_camera_id)
            if weights.get(key) is None:
                weights[key] = 0
            weights[key] += 1
        return DomainPersonFlowWeightSequence(
            flow_weights=[
                DomainPersonFlowWeight(
                    target_camera_id=target_camera_id,
                    source_camera_id=source_camera_id,
                    weight=weight,
                ) for (source_camera_id, target_camera_id), weight in weights.items()
            ],
        )
