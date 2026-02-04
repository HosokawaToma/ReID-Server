from dataclasses import dataclass
from domain.reid.rank import DomainReidRank
from domain.utils.sequence_base import DomainUtilsSequenceBase

@dataclass(frozen=True)
class DomainReidRankSequence(DomainUtilsSequenceBase[DomainReidRank]):
    """
    再識別評価のランクのシーケンスのドメインモデル
    """
    def top_rank(self) -> int:
        """
        最小のランクを取得する
        :return int: 最小のランク
        """
        return min(rank.rank for rank in self.items)

    def sort_by_rank(self) -> "DomainReidRankSequence":
        """
        ランクでソートする
        :return DomainReidRankSequence: ランクでソートしたシーケンス
        """
        return DomainReidRankSequence(items=sorted(self.items, key=lambda x: x.rank))

    def out_camera_id(self, camera_id: int) -> "DomainReidRankSequence":
        """
        カメラIDを除外する
        除外した結果変動するランクを修正する
        :param int camera_id: カメラID
        :return DomainReidRankSequence: カメラIDを除外したシーケンス
        """
        return DomainReidRankSequence(items=[rank for rank in self.items if rank.camera_id != camera_id])

    def out_junk(self) -> "DomainReidRankSequence":
        """
        ゴミデータを除外する
        除外した結果変動するランクを修正する
        :return DomainReidRankSequence: ゴミデータを除外したシーケンス
        """
        return DomainReidRankSequence(items=[rank for rank in self.items if not rank.is_junk])
