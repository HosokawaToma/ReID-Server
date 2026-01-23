from dataclasses import dataclass
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId
from domain.utils.base import DomainUtilsBase

@dataclass
class DomainPersonSnapshotDetail(DomainUtilsBase):
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    person_id: DomainPersonId
