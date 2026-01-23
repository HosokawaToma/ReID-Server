from dataclasses import dataclass
from domain.id import DomainId
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainIdSequence(DomainUtilsSequenceBase[DomainId]):
    pass
