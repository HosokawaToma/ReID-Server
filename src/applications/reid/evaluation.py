"""
再識別評価アプリケーション

指定日のクエリ・ギャラリーを用いてCMC曲線とmAPを計算する。
"""
from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from domain.date import DomainDate
from dto.date import DtoDate
from domain.reid.cmc import DomainReidCmc
from domain.reid.cmc_sequence import DomainReidCmcSequence
from dto.reid.cmc_curve import DtoReidCmcCurve
from dto.id import DtoId
from domain.id_sequence import DomainIdSequence
from error import ValidationError
from domain.reid.ap_sequence import DomainReidApSequence
from domain.reid.ap import DomainReidAp
from dto.reid.map import DtoReidMap
from itertools import chain


class ApplicationReidEvaluation(ApplicationBase):
    """
    再識別評価を行うアプリケーションクラス。

    クエリ・ギャラリーのランキングからCMCとmAPを算出する。
    """

    def __init__(self,
                 repository_person_snapshot: RepositoryPersonSnapshot,
                 ):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationReidEvaluation":
        """
        環境変数からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return ApplicationReidEvaluation: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def calculate(self, date: DtoDate, attempt: int) -> tuple[DtoReidCmcCurve, DtoReidCmcCurve, DtoReidMap, DtoReidMap, list[DtoId]]:
        """
        CMC曲線とmAPを計算する
        CMC曲線は1~50位までを計算する
        ギャラリーデータにゴミデータを含めるケースと含めないケースでそれぞれ計算する
        :param DtoDate date: 日付
        :param int attempt: 試行回数
        :return tuple[DtoReidCmcCurve, DtoReidCmcCurve, DtoReidMap, DtoReidMap, list[DtoId]]: ギャラリーデータにゴミデータを含めないCMC曲線, ギャラリーデータにゴミデータを含めるCMC曲線, ギャラリーデータにゴミデータを含めないmAP, ギャラリーデータにゴミデータを含めるmAP, クエリデータの正解データIDリスト
        """
        query_snapshot_ids = self.repository_person_snapshot.find_query(
            date=DomainDate(year=date.year, month=date.month, day=date.day),
            attempt=attempt,
        )
        query_snapshot_details = self.repository_person_snapshot.find_details_by_ids(
            ids=query_snapshot_ids,
        )
        gallery_rankings_without_junk = self.repository_person_snapshot.find_rankings_without_junk(
            query_snapshot_ids=query_snapshot_ids,
        )
        gallery_rankings_with_junk = self.repository_person_snapshot.find_rankings_with_junk(
            query_snapshot_ids=query_snapshot_ids,
        )
        cmc_sequence_with_junk = DomainReidCmcSequence(items=[])
        cmc_sequence_without_junk = DomainReidCmcSequence(items=[])
        ap_sequence_with_junk = DomainReidApSequence(items=[])
        ap_sequence_without_junk = DomainReidApSequence(items=[])
        for query_snapshot_detail in query_snapshot_details:
            gallery_ranking_with_junk = gallery_rankings_with_junk[query_snapshot_detail.id]
            gallery_ranking_without_junk = gallery_rankings_without_junk[query_snapshot_detail.id]
            cmc_with_junk = DomainReidCmc.calculate(
                gallery_ranking=gallery_ranking_with_junk,
            )
            cmc_without_junk = DomainReidCmc.calculate(
                gallery_ranking=gallery_ranking_without_junk,
            )
            ap_with_junk = DomainReidAp.calculate(
                ranking_sequence=gallery_ranking_with_junk,
            )
            ap_without_junk = DomainReidAp.calculate(
                ranking_sequence=gallery_ranking_without_junk,
            )
            cmc_sequence_with_junk.add(cmc_with_junk)
            ap_sequence_with_junk.add(ap_with_junk)
            cmc_sequence_without_junk.add(cmc_without_junk)
            ap_sequence_without_junk.add(ap_without_junk)

        cmc_curve_with_junk = cmc_sequence_with_junk.to_cmc_curve()
        cmc_curve_without_junk = cmc_sequence_without_junk.to_cmc_curve()
        map_with_junk = ap_sequence_with_junk.average_ap()
        map_without_junk = ap_sequence_without_junk.average_ap()
        return DtoReidCmcCurve(cmc_curve=cmc_curve_with_junk.cmc_curve), DtoReidCmcCurve(cmc_curve=cmc_curve_without_junk.cmc_curve), DtoReidMap(map=map_with_junk.ap), DtoReidMap(map=map_without_junk.ap), [DtoId(id=id.id) for id in query_snapshot_ids]
