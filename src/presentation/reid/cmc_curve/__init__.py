from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.type import PresentationUtilPathDate, PresentationUtilPathInt
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from applications.reid.cmc_curve import ApplicationReidCmcCurve
from dto.date import DtoDate

class PresentationReidCmcCurve(PresentationUtilBase):
    router_path = "/reid/cmc-curve/{date}/{attempt}"
    methods = ["GET"]
    tags = ["reid"]
    summary = "1~50位までのAPを計算しCMC曲線を作成する"
    description = "1~50位までのAPを計算しCMC曲線を作成する"
    responses = {
        200: {
            "description": "1~50位までのAPを計算しCMC曲線を作成する",
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
        attempt: PresentationUtilPathInt,
        application: ApplicationReidCmcCurve = get_application(ApplicationReidCmcCurve),
    ) -> PresentationUtilJSONResponse:
        cmc_curve_is_not_junk, cmc_curve_is_junk, query_person_ids = application.calculate_cmc_curve(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
            attempt=attempt,
        )
        return PresentationUtilJSONResponse(status=200, content={
            "cmc_curve_is_not_junk": cmc_curve_is_not_junk.cmc_curve,
            "cmc_curve_is_junk": cmc_curve_is_junk.cmc_curve,
            "query_person_ids": [str(id.id) for id in query_person_ids],
        })
