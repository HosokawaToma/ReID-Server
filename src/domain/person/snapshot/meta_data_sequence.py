from dataclasses import dataclass
from domain.person.snapshot.meta_data import DomainPersonSnapshotMetaData
from dto.person.snapshot.meta_data import DtoPersonSnapshotMetaData
from typing import Iterator


@dataclass
class DomainPersonSnapshotMetaDataSequence:
    meta_data_list: list[DomainPersonSnapshotMetaData]

    def __iter__(self) -> Iterator[DomainPersonSnapshotMetaData]:
        return iter(self.meta_data_list)

    def to_dto(self) -> list[DtoPersonSnapshotMetaData]:
        return [meta_data.to_dto() for meta_data in self.meta_data_list]
