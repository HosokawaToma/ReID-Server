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


class ApplicationReidEvaluation(ApplicationBase):
    def __init__(self,
                 repository_person_snapshot: RepositoryPersonSnapshot,
                 ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationReidEvaluation":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def calculate(self, date: DtoDate, attempt: int) -> tuple[DtoReidCmcCurve, DtoReidCmcCurve, DtoReidMap, DtoReidMap, list[DtoId]]:
        """
        1~50位までのCMC曲線とmAPを計算する
        ギャラリーデータにゴミデータを含めるケースと含めないケースでそれぞれ計算する
        :param DtoDate date: 日付
        :param int attempt: 試行回数
        :return tuple[DtoReidCmcCurve, DtoReidCmcCurve, DtoReidMap, DtoReidMap, list[DtoId]]: ギャラリーデータにゴミデータを含めないCMC曲線, ギャラリーデータにゴミデータを含めるCMC曲線, ギャラリーデータにゴミデータを含めないmAP, ギャラリーデータにゴミデータを含めるmAP, クエリデータの正解データIDリスト
        """
        query = self.repository_person_snapshot.find_query_is_not_junk(
            date=DomainDate(year=date.year, month=date.month, day=date.day),
            attempt=attempt,
        )
        cmc_sequence_is_not_junk = DomainReidCmcSequence(items=[])
        cmc_sequence_is_junk = DomainReidCmcSequence(items=[])
        ap_sequence_is_not_junk = DomainReidApSequence(items=[])
        ap_sequence_is_junk = DomainReidApSequence(items=[])
        for person_snapshot_id in query:
            person_snapshot_answer = self.repository_person_snapshot.find_answer_label_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            if person_snapshot_answer.person_id.id is None:
                raise ValidationError("正解データが存在しません")
            person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            gallery_answer_labels = self.repository_person_snapshot.find_not_contains_junk_answer_labels_by_person_id(
                person_id=person_snapshot_answer.person_id.id,
            )
            gallery_ranking = self.repository_person_snapshot.find_not_contains_junk_ranking_by_ids(
                person_snapshot_ids=DomainIdSequence(
                    items=[id.id for id in gallery_answer_labels.items]),
                person_snapshot_feature=person_snapshot_feature,
            )
            if not gallery_ranking.items:
                raise ValidationError("ギャラリーデータにゴミデータを含めないランキングが存在しません")
            cmc = DomainReidCmc.calculate(
                gallery_ranking=gallery_ranking,
            )
            ap = DomainReidAp.calculate(
                ranking_sequence=gallery_ranking,
            )
            cmc_sequence_is_not_junk.add(cmc)
            ap_sequence_is_not_junk.add(ap)

        for person_snapshot_id in query:
            person_snapshot_answer = self.repository_person_snapshot.find_answer_label_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            if person_snapshot_answer.person_id.id is None:
                raise ValidationError("正解データが存在しません")
            person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            gallery_answer_labels = self.repository_person_snapshot.find_contains_junk_answer_labels_by_person_id(
                person_id=person_snapshot_answer.person_id.id,
            )
            gallery_ranking = self.repository_person_snapshot.find_contains_junk_ranking_by_ids(
                person_snapshot_ids=DomainIdSequence(
                    items=[id.id for id in gallery_answer_labels.items]),
                person_snapshot_feature=person_snapshot_feature,
            )
            if not gallery_ranking.items:
                raise ValidationError("ギャラリーデータにゴミデータを含めるランキングが存在しません")
            cmc = DomainReidCmc.calculate(
                gallery_ranking=gallery_ranking,
            )
            ap = DomainReidAp.calculate(
                ranking_sequence=gallery_ranking,
            )
            cmc_sequence_is_junk.add(cmc)
            ap_sequence_is_junk.add(ap)

        cmc_curve_is_not_junk = cmc_sequence_is_not_junk.to_cmc_curve()
        cmc_curve_is_junk = cmc_sequence_is_junk.to_cmc_curve()
        map_is_not_junk = ap_sequence_is_not_junk.average_ap()
        map_is_junk = ap_sequence_is_junk.average_ap()
        return DtoReidCmcCurve(cmc_curve=cmc_curve_is_not_junk.cmc_curve), DtoReidCmcCurve(cmc_curve=cmc_curve_is_junk.cmc_curve), DtoReidMap(map=map_is_not_junk.ap), DtoReidMap(map=map_is_junk.ap), [DtoId(id=id.id) for id in query]
