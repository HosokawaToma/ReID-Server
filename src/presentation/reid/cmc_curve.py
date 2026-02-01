from presentation.utils.base import PresentationUtilBase
from typing import Any
from dto.date import DtoDate
from logger import Logger
from presentation.utils.type import PresentationUtilPathDate
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from applications.reid.cmc_curve import ApplicationReidCmcCurve

class PresentationReidCmcCurve(PresentationUtilBase):
    router_path = "/reid/cmc-curve/{date}"
    methods = ["GET"]
    tags = ["reid"]
    summary = "CMC曲線を表示する"
    description = "CMC曲線を表示する"
    responses = {
        200: {
            "description": "CMC曲線を表示する",
        }
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationReidCmcCurve":
        return cls(
            logger=Logger("presentation_reid_cmc_curve"),
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
