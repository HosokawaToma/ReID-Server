from dataclasses import dataclass
from domain.location import DomainLocation
from domain.utils.sequence_base import DomainUtilsSequenceBase

@dataclass(frozen=True)
class DomainLocationSequence(DomainUtilsSequenceBase[DomainLocation]):
    pass
