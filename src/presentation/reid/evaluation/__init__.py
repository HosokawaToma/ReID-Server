"""
再識別評価のプレゼンテーション層

日付・試行回数を受け取り、再識別評価結果をJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.type import PresentationUtilPathDate, PresentationUtilPathInt
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from applications.reid.evaluation import ApplicationReidEvaluation
from dto.date import DtoDate


class PresentationReidEvaluation(PresentationUtilBase):
    """
    再識別評価のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/reid/evaluation/{date}/{attempt}"
    methods = ["GET"]
    tags = ["reid"]
    summary = "再識別評価を行う"
    description = "再識別評価を行う"
    responses = {
        200: {
            "description": "再識別評価を行う",
        }
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationReidEvaluation":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationReidEvaluation: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_reid_evaluation"),
        )

    async def handle(
        self,
        date: PresentationUtilPathDate,
        attempt: PresentationUtilPathInt,
        application: ApplicationReidEvaluation = get_application(
            ApplicationReidEvaluation),
    ) -> PresentationUtilJSONResponse:
        """
        パスから日付・試行回数を取得し、再識別評価を実行して結果を返す。

        :param PresentationUtilPathDate date: 評価対象日
        :param PresentationUtilPathInt attempt: 試行回数
        :param ApplicationReidEvaluation application: 再識別評価アプリケーション
        :return PresentationUtilJSONResponse: CMC曲線・mAP・クエリ正解IDを含むJSONレスポンス
        """
        cmc_curve_with_junk, cmc_curve_without_junk, map_with_junk, map_without_junk, query_person_ids = application.calculate(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
            attempt=attempt,
        )
        return PresentationUtilJSONResponse(status=200, content={
            "cmc_curve_with_junk": cmc_curve_with_junk.cmc_curve,
            "cmc_curve_without_junk": cmc_curve_without_junk.cmc_curve,
            "map_with_junk": map_with_junk.map,
            "map_without_junk": map_without_junk.map,
            "query_person_ids": [str(id.id) for id in query_person_ids],
        })
