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
    再同定評価の CMC（累積マッチング）値を保持するドメインモデル。
    """
    cmc: list[int]

    @classmethod
    def calculate(
        cls,
        gallery_ranking: DomainReidRankSequence,
    ) -> "DomainReidCmc":
        """
        クエリの人物がギャラリー内で何番目に出現するかを計算し、CMC 曲線を作成する。

        CMC は、クエリ画像に対して類似度順に並べたギャラリーの上位 k 位以内に正解が含まれているかを表す指標である。
        複数クエリがあるとき、Rank-k 精度は「各クエリについて、上位 k 枚に正解が含まれていれば 1、含まれていなければ 0 としたときの、全クエリでの平均」として定義される。
        本メソッドは 1 クエリ分のランキングを受け取り、正解が k 位以内に現れていれば k 番目以降の要素を 1 とするベクトルを返す（複数クエリ分を集計するのは呼び出し側で行う）。

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
