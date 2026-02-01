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
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
        )

    def query_is_not_junk_and_gallery_not_contains_junk(self, date: DtoDate) -> tuple[DtoReidCmcCurve, list[DtoId]]:
        """
        クエリデータがゴミデータではなくギャラリーデータにゴミデータが含まれない状況で評価する
        1~50位までのAPを計算しCMC曲線を作成する
        :return tuple[DtoReidCmcCurve, list[DtoId]]: CMC曲線, クエリデータの正解データIDリスト
        """
        query = self.repository_person_snapshot.find_query_is_not_junk(
            date=DomainDate(year=date.year, month=date.month, day=date.day))
        cmc_sequence = DomainReidCmcSequence(items=[])
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
            cmc_sequence.add(cmc)
        cmc_curve = cmc_sequence.to_cmc_curve()
        return DtoReidCmcCurve(cmc_curve=cmc_curve.cmc_curve), [DtoId(id=person_snapshot_id.id) for person_snapshot_id in query]

