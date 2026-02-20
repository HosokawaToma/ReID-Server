"""
再同定評価のプレゼンテーション層

指定した日付・試行回数で再同定（ReID）の評価を実行し、CMC 曲線・mAP・クエリ正解 ID を JSON で返す API を提供する。
GET /reid/evaluation/{date}/{attempt} で呼び出し、評価結果は 200 で返却される。認証は不要。
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
    再同定評価の API エンドポイントを提供するプレゼンテーションクラス。

    パスパラメータで評価対象日（date）と試行回数（attempt）を受け取り、該当する日の人物検出データを用いて
    再同定評価（ゴミ含む・ゴミ除くの CMC 曲線と mAP、およびクエリ正解の人物 ID 一覧）を計算する。
    成功時は 200 とともに JSON（cmc_curve_with_junk, cmc_curve_without_junk, map_with_junk, map_without_junk, query_person_ids）を返す。
    """
    router_path = "/reid/evaluation/{date}/{attempt}"
    methods = ["GET"]
    tags = ["reid"]
    summary = "再同定評価を行う"
    description = "再同定評価を行う"
    responses = {
        200: {
            "description": "再同定評価を行う",
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
        パスから評価対象日と試行回数を取得し、再同定評価を実行して結果を JSON で返す。

        アプリケーション層で指定日の人物検出データに基づく評価（CMC・mAP 計算）を行い、
        ゴミ含み・ゴミ除きの CMC 曲線と mAP、およびクエリ正解の人物 ID 一覧をレスポンスに含める。

        :param PresentationUtilPathDate date: 評価対象日（パス: /reid/evaluation/{date}/{attempt}）
        :param PresentationUtilPathInt attempt: 試行回数（同一日の複数試行を識別する）
        :param ApplicationReidEvaluation application: 再同定評価を行うアプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: ステータス 200、CMC 曲線・mAP・query_person_ids を含む JSON
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
