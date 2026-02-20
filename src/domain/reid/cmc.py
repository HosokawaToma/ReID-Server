"""
ReID CMC（Cumulative Matching Characteristics）のドメインモデル

ギャラリーランキングから CMC ベクトルを算出する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.reid.rank_sequence import DomainReidRankSequence
from error import ValidationError


@dataclass(frozen=True)
class DomainReidCmc(DomainUtilsBase):
    """
    再識別評価の CMC（累積マッチング）値を保持するドメインモデル。
    """
    cmc: list[int]

    @classmethod
    def calculate(
        cls,
        gallery_ranking: DomainReidRankSequence,
    ) -> "DomainReidCmc":
        """
        クエリの人物がギャラリー内で何番目に出現するかを計算し CMC ベクトルを作成する。
        k 番目に出現した場合、k 番目以降を 1 とする。

        :param DomainReidRankSequence gallery_ranking: ギャラリーデータ（クエリに対する類似度順であること）
        :return DomainReidCmc: CMC
        """
        cmc = [0] * 50
        try:
            top_rank = gallery_ranking.top_rank()
        except ValidationError:
            return cls(cmc=cmc)
        if top_rank <= 50:
            start = top_rank - 1
            cmc[start:50] = [1] * (50 - start)
        return cls(cmc=cmc)
