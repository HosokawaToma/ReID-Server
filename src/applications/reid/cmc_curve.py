from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from domain.date import DomainDate
from dto.date import DtoDate
from domain.reid.cmc import DomainReidCmc
from domain.reid.cmc_sequence import DomainReidCmcSequence
from dto.reid.cmc_curve import DtoReidCmcCurve
from dto.id import DtoId


class ApplicationReidCmcCurve(ApplicationBase):
    def __init__(self,
                 repository_person_snapshot: RepositoryPersonSnapshot,
                 ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationReidCmcCurve":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def calculate_cmc_curve(self, date: DtoDate) -> tuple[DtoReidCmcCurve, DtoReidCmcCurve, list[DtoId]]:
        """
        1~50位までのAPを計算しCMC曲線を作成する
        ギャラリーデータにゴミデータを含めるケースと含めないケースでそれぞれ計算する
        :param DtoDate date: 日付
        :return tuple[DtoReidCmcCurve, DtoReidCmcCurve, list[DtoId], list[DtoId]]: ギャラリーデータにゴミデータを含めないCMC曲線, ギャラリーデータにゴミデータを含めるCMC曲線, クエリデータの正解データIDリスト
        """
        query = self.repository_person_snapshot.find_query_is_not_junk(
            date=DomainDate(year=date.year, month=date.month, day=date.day))
        cmc_sequence_is_not_junk = DomainReidCmcSequence(items=[])
        cmc_sequence_is_junk = DomainReidCmcSequence(items=[])
        for person_snapshot_id in query:
            person_snapshot_detail_answer = self.repository_person_snapshot.find_detail_answer_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            if not self.repository_person_snapshot.exists_gallery_not_contains_junk(
                    person_snapshot_detail_answer=person_snapshot_detail_answer):
                continue
            person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            gallery = self.repository_person_snapshot.find_gallery_not_contains_junk(
                person_snapshot_feature=person_snapshot_feature,
            )
            answer_labels = self.repository_person_snapshot.find_answer_labels_by_ids(
                person_snapshot_ids=gallery,
            )
            cmc = DomainReidCmc.calculate(
                query_person_id=person_snapshot_detail_answer.person_id,
                gallery_person_ids=gallery,
                gallery_answer_labels=answer_labels,
            )
            cmc_sequence_is_not_junk.add(cmc)

        for person_snapshot_id in query:
            person_snapshot_detail_answer = self.repository_person_snapshot.find_detail_answer_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            if not self.repository_person_snapshot.exists_gallery_contains_junk(
                    person_snapshot_detail_answer=person_snapshot_detail_answer):
                continue
            person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
                person_snapshot_id=person_snapshot_id,
            )
            gallery = self.repository_person_snapshot.find_gallery_contains_junk(
                person_snapshot_feature=person_snapshot_feature,
            )
            answer_labels = self.repository_person_snapshot.find_answer_labels_by_ids(
                person_snapshot_ids=gallery,
            )
            cmc = DomainReidCmc.calculate(
                query_person_id=person_snapshot_detail_answer.person_id,
                gallery_person_ids=gallery,
                gallery_answer_labels=answer_labels,
            )
            cmc_sequence_is_junk.add(cmc)
        cmc_curve_is_not_junk = cmc_sequence_is_not_junk.to_cmc_curve()
        cmc_curve_is_junk = cmc_sequence_is_junk.to_cmc_curve()
        return DtoReidCmcCurve(cmc_curve=cmc_curve_is_not_junk.cmc_curve), DtoReidCmcCurve(cmc_curve=cmc_curve_is_junk.cmc_curve), [DtoId(id=person_snapshot_id.id) for person_snapshot_id in query]
