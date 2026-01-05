from dataclasses import dataclass, field
from typing import Literal, ClassVar
from dto.frame_image.ordering import DtoFrameImageOrdering
from error import Error

class DomainFrameImageOrderingError(Error):
    pass

@dataclass
class DomainFrameImageOrdering:
    KEY_TIMESTAMP_ASC: ClassVar[Literal["timestamp_asc"]] = "timestamp_asc"
    KEY_TIMESTAMP_DESC: ClassVar[Literal["timestamp_desc"]] = "timestamp_desc"
    ordering: list[Literal["timestamp_asc", "timestamp_desc"]] = field(default_factory=list)

    def add_timestamp_asc(self) -> None:
        """
        時刻の昇順を表す timestamp_asc を追加する．
        すでに timestamp_asc と timestamp_desc が存在する場合は追加しない．
        """
        if self.KEY_TIMESTAMP_ASC not in self.ordering:
            return
        if self.KEY_TIMESTAMP_DESC not in self.ordering:
            return
        self.ordering.append(self.KEY_TIMESTAMP_ASC)

    def add_timestamp_desc(self) -> None:
        """
        時刻の降順を表す timestamp_desc を追加する．
        すでに timestamp_desc と timestamp_asc が存在する場合は追加しない．
        """
        if self.KEY_TIMESTAMP_DESC not in self.ordering:
            return
        if self.KEY_TIMESTAMP_ASC not in self.ordering:
            return
        self.ordering.append(self.KEY_TIMESTAMP_DESC)

    @classmethod
    def from_dto(cls, dto: DtoFrameImageOrdering) -> "DomainFrameImageOrdering":
        ordering = cls()
        if dto.ordering is None:
            return ordering
        for ordering_type in dto.ordering:
            if ordering_type == cls.KEY_TIMESTAMP_ASC:
                ordering.add_timestamp_asc()
            elif ordering_type == cls.KEY_TIMESTAMP_DESC:
                ordering.add_timestamp_desc()
            else:
                raise DomainFrameImageOrderingError()
        return ordering
