from dataclasses import dataclass
from domain.person.snapshot.meta_data import DomainPersonSnapshotMetaData
from typing import Iterator


@dataclass
class DomainPersonSnapshotMetaDataSequence:
    meta_data_list: list[DomainPersonSnapshotMetaData]

    def __iter__(self) -> Iterator[DomainPersonSnapshotMetaData]:
        return iter(self.meta_data_list)
