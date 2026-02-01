from presentation.utils.base import PresentationUtilBase
from typing import Any
from dto.date import DtoDate
from logger import Logger
from presentation.utils.type import PresentationUtilPathDate
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from applications.reid.cmc_curve import ApplicationReidCmcCurve

class PresentationReidCmcCurveQueryIsNotJunkAndGalleryNotContainsJunk(PresentationUtilBase):
    router_path = "/reid/cmc-curve/query-is-not-junk-and-gallery-not-contains-junk/{date}"
    methods = ["GET"]
    tags = ["reid"]
    summary = "クエリデータがゴミデータではなくギャラリーデータにゴミデータが含まれない状況で評価する1~50位までのAPを計算しCMC曲線を作成する"
    description = "クエリデータがゴミデータではなくギャラリーデータにゴミデータが含まれない状況で評価する1~50位までのAPを計算しCMC曲線を作成する"
    responses = {
        200: {
            "description": "クエリデータがゴミデータではなくギャラリーデータにゴミデータが含まれない状況で評価する1~50位までのAPを計算しCMC曲線を作成する",
        }
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationReidCmcCurveQueryIsNotJunkAndGalleryNotContainsJunk":
        return cls(
            logger=Logger("presentation_reid_cmc_curve_query_is_not_junk_and_gallery_not_contains_junk"),
        )

    async def handle(
        self,
        date: PresentationUtilPathDate,
        application: ApplicationReidCmcCurve = get_application(ApplicationReidCmcCurve),
    ) -> PresentationUtilJSONResponse:
        cmc_curve, query_person_ids = application.query_is_not_junk_and_gallery_not_contains_junk(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
        )
        return PresentationUtilJSONResponse(status=200, content={
            "cmc_curve": cmc_curve.cmc_curve,
            "query_person_ids": [str(id.id) for id in query_person_ids],
        })
