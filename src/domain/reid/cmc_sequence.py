"""
ReID CMC シーケンスのドメインモデル

CMC のリストを保持し、平均 CMC 曲線へ変換する。
"""
from dataclasses import dataclass
from domain.reid.cmc import DomainReidCmc
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.reid.cmc_curve import DomainReidCmcCurve


@dataclass(frozen=True)
class DomainReidCmcSequence(DomainUtilsSequenceBase[DomainReidCmc]):
    """
    CMC曲線のシーケンスのドメインモデル
    """

    def to_cmc_curve(self) -> DomainReidCmcCurve:
        """
        各 CMC を平均した CMC 曲線を返す。

        :return DomainReidCmcCurve: 平均 CMC 曲線
        """
        cmc_curve = [0.0] * 50
        if len(self.items) == 0:
            return DomainReidCmcCurve(cmc_curve=cmc_curve)
        for cmc in self.items:
            for i in range(len(cmc.cmc)):
                cmc_curve[i] += cmc.cmc[i]
        return DomainReidCmcCurve(
            cmc_curve=[cmc_curve[i] / len(self.items) for i in range(50)])
