"""
ReID CMC 曲線シーケンスのドメインモデル

複数クエリの CMC 曲線を保持し、平均曲線を算出する。
"""
from dataclasses import dataclass
from domain.reid.cmc_curve import DomainReidCmcCurve
from domain.utils.sequence_base import DomainUtilsSequenceBase


class DomainReidCmcCurveSequence(DomainUtilsSequenceBase[DomainReidCmcCurve]):
    """
    CMC曲線のシーケンスのドメインモデル
    """

    def average_cmc_curve(self) -> DomainReidCmcCurve:
        """
        平均値のCMC曲線を計算する
        :return DomainReidCmcCurve: 平均値のCMC曲線
        """
        cmc_curve = [0.0] * 50
        if len(self.items) == 0:
            return DomainReidCmcCurve(cmc_curve=cmc_curve)
        for cmc_curve_item in self.items:
            for i in range(len(cmc_curve_item.cmc_curve)):
                cmc_curve[i] += cmc_curve_item.cmc_curve[i]
        return DomainReidCmcCurve(cmc_curve=[cmc_curve[i] / len(self.items) for i in range(50)])
