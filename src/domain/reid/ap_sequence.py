"""
ReID AP シーケンスのドメインモデル

AP のリストを保持し、平均 AP（mAP）を算出する。
"""
from dataclasses import dataclass
from domain.reid.ap import DomainReidAp
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainReidApSequence(DomainUtilsSequenceBase[DomainReidAp]):
    """
    APのシーケンスのドメインモデル
    """

    def average_ap(self) -> DomainReidAp:
        """
        APの平均値（mAP）を計算する
        :return DomainReidAp: mAP
        """
        if len(self.items) == 0:
            return DomainReidAp(ap=0.0)
        return DomainReidAp(ap=sum(ap.ap for ap in self.items) / len(self.items))
