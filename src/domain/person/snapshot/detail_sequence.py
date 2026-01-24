from dataclasses import dataclass
from domain.person.snapshot.detail import DomainPersonSnapshotDetail
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.person.flow import DomainPersonFlow
from domain.person.flow.sequence import DomainPersonFlowSequence
from domain.time import DomainTime
from typing import ClassVar

@dataclass(frozen=True)
class DomainPersonSnapshotDetailSequence(DomainUtilsSequenceBase[DomainPersonSnapshotDetail]):
    INTERVAL: ClassVar[DomainTime] = DomainTime(seconds=10)

    def to_flows(self) -> DomainPersonFlowSequence:
        """
        人物検出の集合から人流を計算する
        ある人物がある地点から別の地点に移動した軌跡を生成する
        :return DomainPersonFlowSequence: 人物フローのシーケンス
        """
        if not self.is_flows():
            raise ValueError("人流計算を行える集合ではありません")
        details = self.sort_by_timestamp()
        flows = []
        for i in range(len(details)):
            if i == 0:
                continue
            if details[i].location.camera_id == details[i - 1].location.camera_id \
                and details[i].timestamp - details[i - 1].timestamp <= self.INTERVAL:
                continue
            person_id = details[i].person_id
            if person_id.id is None:
                raise ValueError("人物IDが必要です")
            flows.append(DomainPersonFlow(
                person_id=person_id.id,
                source_location=details[i - 1].location,
                target_location=details[i].location,
                source_timestamp=details[i - 1].timestamp,
                target_timestamp=details[i].timestamp,
            ))
        return DomainPersonFlowSequence(items=flows)

    def is_flows(self) -> bool:
        """
        人物検出の集合から人流を計算できるかどうかを判定する
        人物検出の集合全てが同じ人物IDかつ人物検出が二つ以上必要である
        :return bool: 人流計算できるかどうか
        """
        if len(self.items) < 2:
            return False
        return all(detail.person_id == self.items[0].person_id for detail in self.items)

    def sort_by_timestamp(self) -> "DomainPersonSnapshotDetailSequence":
        """
        人物検出の集合を時間順にソートする
        :return DomainPersonSnapshotDetailSequence: 時間順にソートした人物検出の集合
        """
        return DomainPersonSnapshotDetailSequence(items=sorted(self.items.copy(), key=lambda x: x.timestamp))
