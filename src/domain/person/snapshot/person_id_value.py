from dataclasses import dataclass, field
from domain.id_value import DomainIdValue

@dataclass
class DomainPersonSnapshotPersonIdValue:
    """
    非推奨
    代わりに ValuePersonSnapshotAnnotation を使用する
    人物IDに関するドメイン知識を集約する
    :param DomainIdValue | None person_id: 人物ID
    :param bool is_junk: ジャンクフラグ
    """
    person_id: DomainIdValue | None = field(default=None)
    is_junk: bool = field(default=True)

    @classmethod
    def new_id(cls) -> "DomainPersonSnapshotPersonIdValue":
        return cls(
            person_id=DomainIdValue(),
            is_junk=False,
        )
