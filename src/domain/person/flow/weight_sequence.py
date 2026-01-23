from dataclasses import dataclass
from domain.person.flow.weight import DomainPersonFlowWeight
from domain.utils.sequence_base import DomainUtilsSequenceBase

@dataclass
class DomainPersonFlowWeightSequence(DomainUtilsSequenceBase[DomainPersonFlowWeight]):
    """
    人物フロー重みのシーケンスのドメインモデル
    """
    pass
