from dataclasses import dataclass
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId
from domain.utils.base import DomainUtilsBase


@dataclass
class DomainPersonFlow(DomainUtilsBase):
    """
    個人の移動のドメインモデル
    """
    person_id: DomainPersonId
    source_location: DomainLocation
    target_location: DomainLocation
    source_timestamp: DomainTimestamp
    target_timestamp: DomainTimestamp
