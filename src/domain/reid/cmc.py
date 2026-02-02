from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.reid.rank_sequence import DomainReidRankSequence

@dataclass(frozen=True)
class DomainReidCmc(DomainUtilsBase):
    """
    再識別評価のドメインモデル
    """
    cmc: list[int]

    @classmethod
    def calculate(
        cls,
        gallery_ranking: DomainReidRankSequence,
    ) -> "DomainReidCmc":
        """
        queryの人物がgalleryの中で何番目に出現するかを計算しCMC曲線を作成する
        k番目に出現した場合k番目以降を1とする
        :param DomainReidRankSequence gallery_ranking: ギャラリーデータ（クエリデータに対する類似度順に並んでいることが前提）
        :return DomainReidCmc: CMC
        """
        cmc = [0] * 50
        top_rank = gallery_ranking.top_rank()
        cmc[top_rank:50] = [1] * (50 - top_rank)
        return cls(cmc=cmc)
