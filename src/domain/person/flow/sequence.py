"""
人物フローシーケンスのドメインモデル

フローリストを保持し、地点間の重みシーケンスへ変換する。
"""
from dataclasses import dataclass
from domain.person.flow import DomainPersonFlow
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.person.flow.weight_sequence import DomainPersonFlowWeightSequence
from domain.person.flow.weight import DomainPersonFlowWeight
from domain.location import DomainLocation


@dataclass(frozen=True)
class DomainPersonFlowSequence(DomainUtilsSequenceBase[DomainPersonFlow]):
    """
    人物フローのシーケンスのドメインモデル
    """

    def to_weights(self) -> DomainPersonFlowWeightSequence:
        """
        人物フローのシーケンスから人流の重みを計算する
        ある地点から別の地点に移動した人数をカウントする
        :return DomainPersonFlowWeightSequence: 人物フローのシーケンスから人流の重みを計算したシーケンス
        """
        weights: dict[tuple[DomainLocation, DomainLocation], int] = {}
        for flow in self.items:
            if (flow.source_location, flow.target_location) not in weights:
                weights[(flow.source_location, flow.target_location)] = 0
            weights[(flow.source_location, flow.target_location)] += 1
        return DomainPersonFlowWeightSequence(items=[DomainPersonFlowWeight(
            source_location=source_location,
            target_location=target_location,
            weight=weight,
        ) for (source_location, target_location), weight in weights.items()])
