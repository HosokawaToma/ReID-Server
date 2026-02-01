from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.person.snapshot.person_id_sequence import DomainPersonSnapshotPersonIdSequence
from domain.id_sequence import DomainIdSequence
from domain.person.id import DomainPersonId

@dataclass(frozen=True)
class DomainReidCmc(DomainUtilsBase):
    """
    再識別評価のドメインモデル
    """
    cmc: list[int]

    @classmethod
    def calculate(
        cls,
        query_person_id: DomainPersonId,
        gallery_person_ids: DomainIdSequence,
        gallery_answer_labels: DomainPersonSnapshotPersonIdSequence,
    ) -> "DomainReidCmc":
        """
        queryの人物がgalleryの中で何番目に出現するかを計算しCMC曲線を作成する
        k番目に出現した場合k番目以降を1とする
        :param DomainPersonId query_person_id: クエリデータ
        :param DomainIdSequence gallery_person_ids: ギャラリーデータ（クエリデータに対する類似度順に並んでいることが前提）
        :param DomainPersonSnapshotPersonIdSequence gallery_answer_labels: ギャラリーデータの正解データ
        :return DomainReidCmc: CMC
        """
        cmc = [0] * 50
        if query_person_id.id is None:
            return cls(cmc=cmc)
        if gallery_person_ids.items == []:
            return cls(cmc=cmc)
        if gallery_answer_labels.items == []:
            return cls(cmc=cmc)
        for answer_label in gallery_answer_labels:
            if answer_label.person_id.id == query_person_id.id:
                index = gallery_person_ids.index(answer_label.id)
                cmc[index:50] = [1] * (50 - index)
        return cls(cmc=cmc)
