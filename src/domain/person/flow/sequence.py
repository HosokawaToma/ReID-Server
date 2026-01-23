from dataclasses import dataclass
from domain.person.flow import DomainPersonFlow
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.person.flow.weight_sequence import DomainPersonFlowWeightSequence
from domain.person.flow.weight import DomainPersonFlowWeight
from collections import defaultdict
from domain.location import DomainLocation

@dataclass
class DomainPersonFlowSequence(DomainUtilsSequenceBase[DomainPersonFlow]):
    """
    人物フローのシーケンスのドメインモデル
    """
    def to_weights(self) -> DomainPersonFlowWeightSequence:
        weights: dict[tuple[DomainLocation, DomainLocation], int] = {}
        for flow in self.items:
            if weights.get((flow.source_location, flow.target_location)) is None:
                weights[(flow.source_location, flow.target_location)] = 0
            weights[(flow.source_location, flow.target_location)] += 1
        return DomainPersonFlowWeightSequence(items=[DomainPersonFlowWeight(
            source_location=source_location,
            target_location=target_location,
            weight=weight,
        ) for (source_location, target_location), weight in weights.items()])
